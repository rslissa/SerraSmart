import ast

#pip install pycryptodomex
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


class Encryption:
    def __init__(self):
        with open('cipher_file', 'rb') as c_file:
            self.key = c_file.read(16)
            self.iv = c_file.read(16)

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        ciphertext = cipher.encrypt(pad(str(plaintext).encode('utf-8'), AES.block_size))

        return ciphertext.hex()

    def decrypt(self, ciphertext):
        decipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = unpad(decipher.decrypt(bytes.fromhex(ciphertext)), AES.block_size)

        dict_str = plaintext.decode("UTF-8")
        res = ast.literal_eval(dict_str)

        return res
