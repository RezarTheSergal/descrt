"""
Реализация алгоритма Хаффмана
"""
import csv
import heapq
from collections import defaultdict


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq


class Huffman:
    def __init__(self, frequencies):
        self.frequencies = frequencies
        self.codes = {}
        self.root = None
        
    def encode(self):
        """Построение кодов методом Хаффмана"""
        if len(self.frequencies) == 1:
            # Особый случай: один символ
            char = list(self.frequencies.keys())[0]
            self.codes = {char: "0"}
            return self.codes
        
        # Создаем приоритетную очередь
        heap = [Node(char, freq) for char, freq in self.frequencies.items()]
        heapq.heapify(heap)
        
        # Строим дерево Хаффмана
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(heap, merged)
        
        self.root = heap[0]
        self.codes = {}
        self._build_codes(self.root, "")
        
        return self.codes
    
    def _build_codes(self, node, code):
        """Рекурсивное построение кодов"""
        if node is None:
            return
        
        if node.char is not None:
            self.codes[node.char] = code if code else "0"
            return
        
        self._build_codes(node.left, code + "0")
        self._build_codes(node.right, code + "1")
    
    def save_to_csv(self, output_file='huffman_codes.csv'):
        """Сохранение схемы кодирования в CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Символ', 'Частота', 'Код'])
            
            for char, code in self.codes.items():
                freq = self.frequencies[char]
                writer.writerow([repr(char), f"{freq:.6f}", code])
    
    def calculate_average_length(self):
        """Вычисление средней длины кода"""
        avg_length = sum(
            self.frequencies[char] * len(code)
            for char, code in self.codes.items()
        )
        return avg_length
    
    def calculate_efficiency(self, entropy):
        """Вычисление эффективности сжатия"""
        avg_length = self.calculate_average_length()
        efficiency = (entropy / avg_length) * 100 if avg_length > 0 else 0
        return efficiency
    
    def encode_text(self, text):
        """Кодирование текста"""
        return ''.join(self.codes.get(char, '') for char in text)
    
    def decode_text(self, encoded_text):
        """Декодирование текста"""
        decoded = []
        current_node = self.root
        
        for bit in encoded_text:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
            
            if current_node.char is not None:
                decoded.append(current_node.char)
                current_node = self.root
        
        return ''.join(decoded)
