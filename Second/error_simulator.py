import random


class ErrorSimulator:
    @staticmethod
    def make_an_error(bits, position=None):
        if not bits:
            raise ValueError("Пустая битовая строка")
        
        if position is None:
            position = random.randint(0, len(bits) - 1)
        elif position < 0 or position >= len(bits):
            raise ValueError(f"Позиция {position} вне диапазона [0, {len(bits)-1}]")
        
        bits_list = list(bits)
        bits_list[position] = '0' if bits_list[position] == '1' else '1'
        
        return ''.join(bits_list), position + 1  # возвращаем 1-based позицию
