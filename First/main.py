"""
Главный файл программы для анализа текста и кодирования
"""
import argparse
from text_analyzer import TextAnalyzer
from shannon_fano import ShannonFano
from huffman import Huffman
from bigram_analyzer import BigramAnalyzer
from pathlib import Path

def main(args):
    save_directory_path = Path(__file__).resolve().parent / "Output"
    print("\nСтатистика чистого текста:")
    # 1-3.
    analyzer = TextAnalyzer(args.filename)
    text = analyzer.read_text()
    print(f"Длина текста: {len(text)} с.")
    
    alphabet = analyzer.build_alphabet()
    print(f"Размер алфавита: {len(alphabet)} с.")
    
    analyzer.save_alphabet_to_csv((save_directory_path / 'alphabet.csv').__str__())
    # 4-6.
    entropy = analyzer.calculate_entropy()

    print("\nСтатистика:")
    analyzer.print_stats()
    
    # 8-12.
    print("\nШенон-Фано (одн. б):")
    
    sf = ShannonFano(analyzer.get_frequency_dict())
    sf.encode()
    sf.save_to_csv((save_directory_path / 'shannon_fano_single.csv').__str__())
    
    sf_avg_length = sf.calculate_average_length()
    sf_efficiency = sf.calculate_efficiency(entropy)
    
    print(f"Средняя длина кода: {sf_avg_length:.4f} бит/c.")
    print(f"Эффективность сжатия: {sf_efficiency:.2f}%")
    
    # 13-14.
    encoded_sf = sf.encode_text(text)
    with open((save_directory_path / 'encoded_shannon_fano.txt').__str__(), 'w') as f:
        f.write(encoded_sf)
    print(f"Текст закодирован")
    
    # 15-16.
    decoded_sf = sf.decode_text(encoded_sf)
    with open((save_directory_path / 'decoded_shannon_fano.txt').__str__(), 'w', encoding='utf-8') as f:
        f.write(decoded_sf)
    
    if decoded_sf == text:
        print("Декодирование выполнено корректно!")
    else:
        print("Ошибка декодирования!")
    
    # 17.
    print("\nШенон-Фано (дву. б):")
    
    bigram_analyzer = BigramAnalyzer(text)
    bigrams = bigram_analyzer.build_bigrams()
    print(f"Построено {len(bigrams)} биграмм")
    
    sf_bigram = ShannonFano(bigram_analyzer.bigrams)
    sf_bigram.encode()
    sf_bigram.save_to_csv((save_directory_path / 'shannon_fano_bigram.csv').__str__())
    print("Схема кодирования биграмм сохранена")
    
    # 18.
    print("\nХаффман (одн. б)")
    
    hf = Huffman(analyzer.get_frequency_dict())
    hf.encode()
    hf.save_to_csv((save_directory_path / 'huffman_single.csv').__str__())
    print("Схема кодирования сохранена в huffman_single.csv")
    
    hf_avg_length = hf.calculate_average_length()
    hf_efficiency = hf.calculate_efficiency(entropy)
    
    print(f"Средняя длина кода: {hf_avg_length:.4f} бит/с.")
    print(f"Эффективность сжатия: {hf_efficiency:.2f}%")
    
    # Кодирование и декодирование Хаффманом
    encoded_hf = hf.encode_text(text)
    with open((save_directory_path / 'encoded_huffman.txt').__str__(), 'w') as f:
        f.write(encoded_hf)
    print(f"Текст закодирован")
    
    decoded_hf = hf.decode_text(encoded_hf)
    with open((save_directory_path / 'decoded_huffman.txt').__str__(), 'w', encoding='utf-8') as f:
        f.write(decoded_hf)
    
    if decoded_hf == text:
        print("Декодирование выполнено корректно!")
    else:
        print("Ошибка декодирования!")
    
    print("\nХаффман (дву. б)")
    
    hf_bigram = Huffman(bigram_analyzer.get_frequency_dict())
    hf_bigram.encode()
    hf_bigram.save_to_csv((save_directory_path / 'huffman_bigram.csv').__str__())
    print("Схема кодирования биграмм сохранена")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Имя файла для обработки')
    
    args = parser.parse_args()
    main(args)