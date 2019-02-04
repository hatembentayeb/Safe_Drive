# ch9_decrypt_blob.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import zlib

class D_Data():
    # Our Decryption Function
    def decrypt_blob(self,encrypted_blob, private_key):
        # Import the Private Key and use for decryption using PKCS1_OAEP
        rsakey = RSA.importKey(private_key)
        rsakey = PKCS1_OAEP.new(rsakey)

        # Base 64 decode the data
        encrypted_blob = base64.b64decode(encrypted_blob)

        # In determining the chunk size, determine the private key length used in bytes.
        # The data will be in decrypted in chunks
        chunk_size = 512
        offset = 0
        decrypted = b""

        # keep loop going as long as we have chunks to decrypt
        while offset < len(encrypted_blob):
            # The chunk
            chunk = encrypted_blob[offset: offset + chunk_size]

            # Append the decrypted chunk to the overall decrypted file
            decrypted += rsakey.decrypt(chunk)

            # Increase the offset by chunk size
            offset += chunk_size

        # return the decompressed decrypted data
        return zlib.decompress(decrypted)

    def do_the_job(self,filename):
        # Use the private key for decryption
        with open(".keys/private_key.pem", "rb") as fd:
            private_key = fd.read()

        # Our candidate file to be decrypted
        with open(filename, "rb") as fd:
            encrypted_blob = fd.read()

        # Write the decrypted contents to a file
        with open("decrypted_{}".format(filename), "wb") as fd:
            fd.write(self.decrypt_blob(encrypted_blob, private_key))
