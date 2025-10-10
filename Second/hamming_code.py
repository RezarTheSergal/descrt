"""
Класс для работы с кодом Хемминга
"""
import numpy as np


class HammingCode:
    def __init__(self, r, l):
        """
        Инициализация кода Хемминга
        r - количество проверочных битов
        l - изначальная длинна слова
        """
        self.l = l
        self.r = r
        self.n = 2**r - 1  # общая длина кодового слова
        self.k = self.n - r  # количество информационных битов
        self.parity_matrix = self._generate_parity_matrix()
    
    def _generate_parity_matrix(self):
        """Генерация проверочной матрицы H"""
        matrix = []
        for i in range(self.r):
            row = []
            for pos in range(1, self.n + 1):
                # Проверяем, участвует ли позиция pos в проверочном бите 2^i
                if pos & (1 << i):
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return np.array(matrix)
    
    def get_parity_positions(self):
        """Возвращает позиции проверочных битов (степени двойки)"""
        return [2**i for i in range(self.r)]
    
    def print_table(self):
        """Вывод проверочной таблицы"""
        print(f"  П-и: {' '.join(f'{i+1:2d}' for i in range(self.n))}")
        for i, row in enumerate(self.parity_matrix):
            print(f"   r{i+1}: {' '.join(f'{bit:2d}' for bit in row)}")
    
    def encode(self, data_bits):
        """
        Кодирование информационных битов
        data_bits - строка из '0' и '1'
        """
        if len(data_bits) > self.k:
            raise ValueError(f"Слишком много битов. Максимум: {self.k}")
        
        # Создаём кодовое слово с нулями
        code_word = [0] * self.n
        data_idx = 0
        
        # Размещаем информационные биты (пропускаем позиции степеней двойки)
        for pos in range(1, self.n + 1):
            if pos & (pos - 1) != 0:  # не степень двойки
                if data_idx < len(data_bits):
                    code_word[pos - 1] = int(data_bits[data_idx])
                    data_idx += 1
        
        # Вычисляем проверочные биты
        for i in range(self.r):
            parity_pos = (1 << i) - 1  # 2^i - 1 (позиция в массиве)
            parity = 0
            
            # Суммируем биты, контролируемые этим проверочным битом
            for pos in range(self.n):
                if self.parity_matrix[i][pos] == 1 and pos != parity_pos:
                    parity ^= code_word[pos]
            
            code_word[parity_pos] = parity
        
        return ''.join(str(b) for b in code_word)
    
    def calculate_syndrome(self, received_bits):
        """Вычисление синдрома для поиска ошибки"""
        syndrome = 0
        received = [int(b) for b in received_bits]
        
        for i in range(self.r):
            parity = 0
            for pos in range(self.n):
                if self.parity_matrix[i][pos] == 1:
                    parity ^= received[pos]
            syndrome |= (parity << i)
        
        return syndrome
    
    def correct_error(self, received_bits, syndrome):
        """Исправление ошибки на основе синдрома"""
        if syndrome == 0:
            return received_bits
        
        received_list = list(received_bits)
        error_pos = syndrome - 1  # синдром указывает на позицию (1-based)
        
        if 0 <= error_pos < len(received_list):
            received_list[error_pos] = '0' if received_list[error_pos] == '1' else '1'
        
        return ''.join(received_list)
    
    def decode(self, code_word):
        """Извлечение информационных битов из кодового слова"""
        data_bits = []
        
        for pos in range(1, self.n + 1):
            if pos & (pos - 1) != 0:  # не степень двойки
                data_bits.append(code_word[pos - 1])

        return ''.join([bit for i, bit in enumerate(data_bits) if i < self.l])