from Crypto.PublicKey import RSA
from termcolor import colored
from binascii import hexlify

class Genkey():
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        # Generate a public/ private key pair using 4096 bits key length (512 bytes)
        new_key = RSA.generate(4096, e=65537)
        # The private key in PEM format
        self.private_key = new_key.exportKey("PEM")
        # The public key in PEM Format
        self.public_key = new_key.publickey().exportKey("PEM")

    def print_keys(self):
        print(colored(self.private_key.decode('ascii'), "blue"))
        with open(".keys/private_key.pem", "wb") as fd:
            fd.write(self.private_key)
        print("\n\n")
        print(colored(self.public_key.decode('ascii'), "blue"))
        with open(".keys/public_key.pem", "wb") as fd:
            fd.write(self.public_key)

