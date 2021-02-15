from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import ast
import sys


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

'''
if __name__ == '__main__':
    from datetime import datetime
    msg = {
        "message": {
            "id": 220,
            "datetime": str(datetime.now()),
            "acquisition_point": "A01",
            "EC": 742.923000977200,
            "WF": 4.78589726070381,
            "GT": 742.923000977200,
            "GH": None,
            "AT": 742.923000977200,
            "AH": None
        }
    }
    print('Testo di input', msg)
    enc = Encryption()
    p1 = enc.encrypt(msg)
    print('Testo criptato', p1)

    p2 = enc.decrypt(p1)
    print('Testo decifrato', p2)

    if msg == p2:
        print('Testi uguali')

    # print(sys.getsizeof(ciphertext))'''
