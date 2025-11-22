import random
from typing import List, Tuple

class PseudoRandomGenerator:
    """Генератор псевдослучайных чисел (линейный конгруэнтный метод)"""
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        # Параметры LCG (как в glibc)
        self.a = 1103515245
        self.c = 12345
        self.m = 2**31
        self.current = seed
    
    def next(self) -> int:
        """Генерирует следующее псевдослучайное число"""
        self.current = (self.a * self.current + self.c) % self.m
        return self.current
    
    def next_byte(self) -> int:
        """Генерирует псевдослучайный байт (0-255)"""
        return self.next() % 256


class GammaCipher:
    """Шифр гаммирования (XOR-шифрование)"""
    
    def __init__(self, seed: int = 42):
        self.generator = PseudoRandomGenerator(seed)
    
    def generate_gamma(self, length: int) -> List[int]:
        """Генерирует гамму заданной длины"""
        return [self.generator.next_byte() for _ in range(length)]
    
    def encrypt(self, plaintext: str) -> Tuple[bytes, List[int]]:
        """
        Шифрует открытый текст
        Возвращает: (зашифрованные байты, использованная гамма)
        """
        plaintext_bytes = plaintext.encode('utf-8')
        gamma = self.generate_gamma(len(plaintext_bytes))
        
        # XOR каждого байта с соответствующим байтом гаммы
        ciphertext = bytes(pb ^ g for pb, g in zip(plaintext_bytes, gamma))
        
        return ciphertext, gamma
    
    def decrypt(self, ciphertext: bytes, gamma: List[int]) -> str:
        """Дешифрует зашифрованный текст используя гамму"""
        # XOR работает в обе стороны: encrypt = decrypt
        plaintext_bytes = bytes(cb ^ g for cb, g in zip(ciphertext, gamma))
        return plaintext_bytes.decode('utf-8')
