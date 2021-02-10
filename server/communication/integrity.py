import hashlib
import hmac
import communication.default as df


class Integrity:
    def __init__(self):
        self.password = df.PASSWORD

    def get_digest(self, msg):
        digest = None
        if msg is not None:
            m = hmac.new(self.password, digestmod=hashlib.blake2s)
            m.update(str(msg).encode('utf-8'))  # possiamo chiamarla iterativamente più volte per aumentare la sicurezza
            digest = m.hexdigest()

        return digest

    def compare_digest(self, tx, rx):
        if tx == rx:
            return True
        else:
            return False
