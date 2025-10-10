"""
Симулятор ошибок в битовых последовательностях
"""
import random


class ErrorSimulator:
    def __init__(self, seed=None):
        """
        Инициализация симулятора ошибок
        seed - для воспроизводимости (опционально)
        """
        if seed is not None:
            random.seed(seed)
    
    def introduce_error(self, bits, position=None):
        """
        Внесение однобитовой ошибки
        bits - битовая строка
        position - конкретная позиция (если None, выбирается случайно)
        Возвращает: (изменённая строка, позиция ошибки)
        """
        if not bits:
            raise ValueError("Пустая битовая строка")
        
        if position is None:
            position = random.randint(0, len(bits) - 1)
        elif position < 0 or position >= len(bits):
            raise ValueError(f"Позиция {position} вне диапазона [0, {len(bits)-1}]")
        
        bits_list = list(bits)
        bits_list[position] = '0' if bits_list[position] == '1' else '1'
        
        return ''.join(bits_list), position + 1  # возвращаем 1-based позицию
    
    def introduce_multiple_errors(self, bits, count):
        """Внесение множественных ошибок (для тестирования)"""
        positions = random.sample(range(len(bits)), min(count, len(bits)))
        bits_list = list(bits)
        
        for pos in positions:
            bits_list[pos] = '0' if bits_list[pos] == '1' else '1'
        
        return ''.join(bits_list), [p + 1 for p in positions]
