import csv
from collections import Counter
from math import log2


class TextAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.text = ""
        self.alphabet = {}
        self.entropy = 0
        
    def read_text(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.text = f.read()
        return self.text
    
    def build_alphabet(self):
        counter = Counter(self.text)
        total = len(self.text)
        
        self.alphabet = {
            char: {
                'count': count,
                'frequency': count / total
            }
            for char, count in counter.items()
        }
        
        # Сортировка по частоте от > к <
        self.alphabet = dict(sorted(
            self.alphabet.items(), 
            key=lambda x: x[1]['frequency'], 
            reverse=True
        ))
        
        return self.alphabet
    
    def save_alphabet_to_csv(self, output_file='alphabet.csv'):
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
        self.entropy = -sum(
            data['frequency'] * log2(data['frequency'])
            for data in self.alphabet.values()
            if data['frequency'] > 0
        )
        return self.entropy
    
    # Равномерное кодирование
    def calculate_uniform_code_length(self):
        alphabet_size = len(self.alphabet)
        uniform_code_length = log2(alphabet_size)
        return uniform_code_length
    
    def calculate_redundancy(self):
        redundancy = self.calculate_uniform_code_length() - self.entropy
        return redundancy
    
    def print_stats(self):
        print(f"Энтропия: {self.entropy:.4f} бит/с.")
        print(f"Длина кода при равномерном кодировании: {self.calculate_uniform_code_length():.4f} бит")
        print(f"Избыточность: {self.calculate_redundancy():.4f} бит")
    
    def get_frequency_dict(self):
        return {char: data['frequency'] for char, data in self.alphabet.items()}
