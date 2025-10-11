"""
Генератор случайных битовых последовательностей
"""
import random


class BitGenerator:
    @staticmethod
    def generate(length):
        return ''.join(random.choice('01') for _ in range(length))
    
    @staticmethod
    def generate_from_text(text):
        """Конвертация текста в биты (если понадобится)"""
        return ''.join(format(ord(char), '08b') for char in text)
