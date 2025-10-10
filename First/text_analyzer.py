"""
Класс для анализа текста и вычисления информационных характеристик
"""
import csv
from collections import Counter
from math import log2


class TextAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.text = ""
        self.alphabet = {}
        self.entropy = 0
        self.uniform_code_length = 0
        self.redundancy = 0
        
    def read_text(self):
        """Чтение текста из файла"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.text = f.read()
        return self.text
    
    def build_alphabet(self):
        """Создание алфавита с частотами символов"""
        counter = Counter(self.text)
        total = len(self.text)
        
        self.alphabet = {
            char: {
                'count': count,
                'frequency': count / total
            }
            for char, count in counter.items()
        }
        
        # Сортировка по частоте
        self.alphabet = dict(sorted(
            self.alphabet.items(), 
            key=lambda x: x[1]['frequency'], 
            reverse=True
        ))
        
        return self.alphabet
    
    def save_alphabet_to_csv(self, output_file='alphabet.csv'):
        """Сохранение алфавита в CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Символ', 'Количество', 'Частота'])
            
            for char, data in self.alphabet.items():
                writer.writerow([
                    repr(char), 
                    data['count'], 
                    f"{data['frequency']:.8f}"
                ])
    
    def calculate_entropy(self):
        """Вычисление энтропии"""
        self.entropy = -sum(
            data['frequency'] * log2(data['frequency'])
            for data in self.alphabet.values()
            if data['frequency'] > 0
        )
        return self.entropy
    
    def calculate_uniform_code_length(self):
        """Длина кода при равномерном кодировании"""
        alphabet_size = len(self.alphabet)
        self.uniform_code_length = log2(alphabet_size)
        return self.uniform_code_length
    
    def calculate_redundancy(self):
        """Вычисление избыточности"""
        self.redundancy = self.uniform_code_length - self.entropy
        return self.redundancy
    
    def print_stats(self):
        """Вывод статистики в консоль"""
        print(f"Энтропия: {self.entropy:.4f} бит/символ")
        print(f"Длина кода при равномерном кодировании: {self.uniform_code_length:.4f} бит")
        print(f"Избыточность: {self.redundancy:.4f} бит")
    
    def get_frequency_dict(self):
        """Получение словаря частот для кодирования"""
        return {char: data['frequency'] for char, data in self.alphabet.items()}
