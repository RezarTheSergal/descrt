"""
Класс для работы с двухбуквенными сочетаниями (биграммами)
"""
from collections import Counter


class BigramAnalyzer:
    def __init__(self, text):
        self.text = text
        self.bigrams = {}
        
    def build_bigrams(self):
        bigram_list = [
            self.text[i:i+2] 
            for i in range(len(self.text) - 1)
        ]
        
        counter = Counter(bigram_list)
        total = len(bigram_list)
        
        self.bigrams = {
            bigram: count / total for bigram, count in counter.items()
        }
        
        # Сортировка по частоте
        self.bigrams = dict(sorted(
            self.bigrams.items(), 
            key=lambda x: x[1], 
            reverse=True
        ))
        
        return self.bigrams
