# core/interfaces.py
from abc import ABC, abstractmethod

class BaseCipher(ABC):
    """
    The Blueprint. Any cipher you want to test MUST follow these rules.
    """
    
    @property
    @abstractmethod
    def name(self):
        """Return the name of the Cipher (e.g., 'Ascon-128')"""
        pass

    @abstractmethod
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Core encryption logic"""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Core decryption logic"""
        pass