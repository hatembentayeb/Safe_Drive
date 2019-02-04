from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from termcolor import colored
from generate_keys import Genkey
import os
import readline

from encrypt_data import C_Data
from decryt_data import D_Data

os.system('clear')
print(colored('''
  _____                      _            _         _____     _ _                      
 / ____|                    (_)          | |       |_   _|   (_) |                     
| (___   ___  ___ _   _ _ __ _ _ __   ___| |_ ___    | |  ___ _| |_ ___ ___  _ __ ___  
 \___ \ / _ \/ __| | | | '__| | '_ \ / _ \ __/ __|   | | / __| | __/ __/ _ \| '_ ` _ \ 
 ____) |  __/ (__| |_| | |  | | | | |  __/ |_\__ \  _| |_\__ \ | || (_| (_) | | | | | |
|_____/ \___|\___|\__,_|_|  |_|_| |_|\___|\__|___/ |_____|___/_|\__\___\___/|_| |_| |_|\n''', 'blue'),
      colored('Keep your data safe', 'red', attrs=['blink']))

print(colored('\n[+] Crypt your data and save them on Drive', 'yellow'))
print(colored('[+] Be Safe !\n', 'yellow'))

addrs = ['auth', 'help', 'upload', 'genkeys', 'list', 'exit','download',]

def completer(text, state):
    options = [x for x in addrs if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

while True:

    command = input(colored("\nSecurinets# ", "red", attrs=['bold']))
    command = command.split(" ")

    if (command[0] == "help"):
        print(colored('''\n
 usage: command [arguments]
      
      :help: print this message
      :auth: authentificate with your account
      :upload: upload existant file or create on
      :download: download file from the drive ==> download  filename file_id
      :list: get list of files of your drive storage
      :genKeys: generate public and private keys
      \n''', 'green'))

    if (command[0] == "auth"):
        # authentification
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

    if (command[0] == "upload" and len(command) > 1):

        drive = GoogleDrive(gauth)
        if (os.path.isfile(command[1].lstrip())):
            filename = command[1]
            print(colored("\n[+] encrypting file ...", "green"))
            crypt_Data = C_Data()
            crypt_Data.do_the_job(filename.lstrip())
            print(colored("[+] files is crypted !", "blue"))
            print(colored("[+] start uploading ...", "green"))
            file1 = drive.CreateFile()
            file1.SetContentFile("encrypted_" + filename)  # Set content of the file from given string.
            file1.Upload()
            print(colored("[+] uploading file succussfully!\n", 'blue'))
        else:
            print(colored("[-] file does not exist !\n", "red"))

    if (command[0] == "download" and len(command) > 2):
        try:
            drive = GoogleDrive(gauth)
            filename = command[1].lstrip()
            id=command[2].lstrip()
            print(colored("\n[+] start downloading ...", "green"))
            file1 = drive.CreateFile({'id': id})
            file1.GetContentFile(filename)
            print(colored("[+] file successfully downloaded ...", "cyan"))
            print(colored("[+] start decrypting file ...", "green"))
            decrypt_Data = D_Data()
            decrypt_Data.do_the_job(filename)
            os.system("rm "+filename)
            print(colored("[+] files  decrypted successefully!\n", "blue"))
        except Exception:
            print(colored("[-] ERROR! file name dose not exit or run auth command .. please check\n", "red"))





    if (command[0] == "list"):
        try:
            drive = GoogleDrive(gauth)
            print(colored("[*] Start updating files list from google drive ...", "cyan"))
            os.system("rm file_list.txt")
            file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
            for file1 in file_list:
                print("NAME : ( {} ) ==> ID : ( {} )".format(file1['title'],file1['id']))
                with open("file_list.txt",'a') as f:
                    f.write("NAME : ( {} ) ==> ID : ( {} )\n".format(file1['title'],file1['id']))
            print(colored("[+] files updated successfully ! \n", "green"))

        except Exception:
            print(colored("\n[-] you must run auth command ...",'red'))


    if (command[0] == "genkeys"):
        if(os.path.isfile(".keys/private_key.pem") and os.path.isfile(".keys/public_key.pem") ):

            print(colored("\n[*] keys already exists.\n", "cyan"))
        else:
            print(colored("\n[+] generating keys...\n", "green"))
            genkey = Genkey()
            genkey.create_keys()
            genkey.print_keys()

    if (command[0] == "exit"):
        print(colored("\n[OK] quitting ...", "magenta"))
        os.system("rm file_list.txt")
        print(colored("[OK] cleaning ...\n", "magenta"))
        exit(1)
