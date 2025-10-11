import csv
from typing import Any


class ShannonFano:
    def __init__(self, frequencies: dict[str, Any]):
        self.frequencies = frequencies
        self.codes = {}
        
    def encode(self):
        sorted_items = sorted(
            self.frequencies.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        self.codes = {}
        self._build_codes(sorted_items, "")
        return self.codes
    
    def _build_codes(self, items, prefix):
        if len(items) == 1:
            self.codes[items[0][0]] = prefix if prefix else "0"
            return
        
        if len(items) == 2:
            self.codes[items[0][0]] = prefix + "0"
            self.codes[items[1][0]] = prefix + "1"
            return
        
        # Находим точку разделения
        total = sum(freq for _, freq in items)
        cumsum = 0
        split_index = 0
        min_diff = float('inf')
        
        for i in range(len(items) - 1):
            cumsum += items[i][1]
            diff = abs(2 * cumsum - total)
            if diff < min_diff:
                min_diff = diff
                split_index = i + 1
        
        # Рекурсивно кодируем две группы
        self._build_codes(items[:split_index], prefix + "0")
        self._build_codes(items[split_index:], prefix + "1")
    
    def save_to_csv(self, output_file='shannon_fano_codes.csv'):
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Символ', 'Частота', 'Код'])
            
            for char, code in self.codes.items():
                freq = self.frequencies[char]
                writer.writerow([repr(char), f"{freq:.6f}", code])
    
    def calculate_average_length(self):
        avg_length = sum(
            self.frequencies[char] * len(code)
            for char, code in self.codes.items()
        )
        return avg_length
    
    def calculate_efficiency(self, entropy):
        avg_length = self.calculate_average_length()
        efficiency = (entropy / avg_length) * 100 if avg_length > 0 else 0
        return efficiency
    
    def encode_text(self, text):
        return ''.join(self.codes.get(char, '') for char in text)
    
    def decode_text(self, encoded_text):
        reverse_codes = {code: char for char, code in self.codes.items()}
        
        decoded = []
        current_code = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_codes:
                decoded.append(reverse_codes[current_code])
                current_code = ""
        
        return ''.join(decoded)
