from hashlib import sha256
import os
from termcolor import colored
import base64
class hashFile():
    def __init__(self):
        self.hash_file=None
        self.name=None



    def make_hash(self,filename):
        if (os.path.isfile(filename)):
            with open(filename,'r') as f:
                content = f.read().encode()

            self.hashed_file = sha256(base64.b64encode(content)).hexdigest()
            self.name = filename

            print(colored('{} --> {}'.format(filename,self.hashed_file),'cyan'))
            with open("saved_hashs.txt",'a') as f:
                f.write('{} --> {}\n'.format(filename,self.hashed_file))


hhh = hashFile()
hhh.make_hash('test.py')