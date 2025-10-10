"""
Генератор случайных битовых последовательностей
"""
import random


class BitGenerator:
    def __init__(self, seed=None):
        """
        Инициализация генератора
        seed - для воспроизводимости результатов (опционально)
        """
        if seed is not None:
            random.seed(seed)
    
    def generate(self, length):
        """
        Генерация случайной битовой последовательности
        length - количество битов
        """
        return ''.join(random.choice('01') for _ in range(length))
    
    def generate_from_text(self, text):
        """Конвертация текста в биты (если понадобится)"""
        return ''.join(format(ord(char), '08b') for char in text)
