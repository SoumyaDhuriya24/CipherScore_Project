from core.interfaces import BaseCipher

class SimpleXORCipher(BaseCipher):
    @property
    def name(self):
        return "Simple XOR (Weak)"

    def encrypt(self, plaintext, key):
        # A very weak cipher just for testing the pipeline
        return bytes([p ^ k for p, k in zip(plaintext, key)])

    def decrypt(self, ciphertext, key):
        return self.encrypt(ciphertext, key)