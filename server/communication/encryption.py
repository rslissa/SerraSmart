from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import ast
import communication.validation as validator
import sys


class Encryption:
    def __init__(self):
        with open('cipher_file', 'rb') as c_file:
            self.key = c_file.read(16)
            self.iv = c_file.read(16)

    def encrypt(self, plaintext):
        if validator.validBody(plaintext):
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            ciphertext = cipher.encrypt(pad(str(plaintext).encode('utf-8'), AES.block_size))
        else:
            return 'Message not valid'

        return ciphertext.hex()

    def decrypt(self, ciphertext):
        try:
            decipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            plaintext = unpad(decipher.decrypt(bytes.fromhex(ciphertext)), AES.block_size)

            dict_str = plaintext.decode("UTF-8")
            res = ast.literal_eval(dict_str)
        except:
            print('Message not good to be decrypted!')
            return None

        return res

'''
if __name__ == '__main__':
    from datetime import datetime
    msg = {
        "message": {
            "id": 112,
            "datetime": str(datetime.now()),
            "acquisition_point": "A01",
            "EC": 2500,
            "WF": 558.2,
            "GT": 0.0,
            "GH": 80.0,
            "AT": 7898585.0,
            "AH": 5000000.0
        }
    }
    print('Testo di input', msg)
    enc = Encryption()
    p1 = enc.encrypt(msg)
    print('Testo criptato', p1)
    print(len(p1), type(p1))

    p2 = enc.decrypt(p1)
    print('Testo decifrato', p2)

    if msg == p2:
        print('Testi uguali')

    print(sys.getsizeof(p1))
'''
