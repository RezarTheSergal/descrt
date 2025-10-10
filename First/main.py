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
    # Ввод имени файла
    save_directory_path = Path(__file__).resolve().parent / "Output"
    print("\n=== АНАЛИЗ ТЕКСТА ===\n")
    
    # 1-3. Чтение текста и создание алфавита
    analyzer = TextAnalyzer(args.filename)
    text = analyzer.read_text()
    print(f"Текст прочитан. Длина: {len(text)} символов")
    
    alphabet = analyzer.build_alphabet()
    print(f"Алфавит построен. Размер: {len(alphabet)} символов")
    
    analyzer.save_alphabet_to_csv((save_directory_path / 'alphabet.csv').__str__())
    print("Алфавит сохранен в alphabet.csv")
    
    # 4-6. Вычисление характеристик
    entropy = analyzer.calculate_entropy()
    uniform_length = analyzer.calculate_uniform_code_length()
    redundancy = analyzer.calculate_redundancy()
    
    print("\n=== СТАТИСТИКА ===\n")
    analyzer.print_stats()
    
    # 8-12. Кодирование методом Шеннона-Фано
    print("\n=== МЕТОД ШЕННОНА-ФАНО (ОДНОБУКВЕННЫЕ) ===\n")
    
    sf = ShannonFano(analyzer.get_frequency_dict())
    sf.encode()
    sf.save_to_csv((save_directory_path / 'shannon_fano_single.csv').__str__())
    print("Схема кодирования сохранена в shannon_fano_single.csv")
    
    sf_avg_length = sf.calculate_average_length()
    sf_efficiency = sf.calculate_efficiency(entropy)
    
    print(f"Средняя длина кода: {sf_avg_length:.4f} бит/символ")
    print(f"Эффективность сжатия: {sf_efficiency:.2f}%")
    
    # 13-14. Кодирование текста
    encoded_sf = sf.encode_text(text)
    with open((save_directory_path / 'encoded_shannon_fano.txt').__str__(), 'w') as f:
        f.write(encoded_sf)
    print(f"Текст закодирован ({len(encoded_sf)} бит) и сохранен в encoded_shannon_fano.txt")
    
    # 15-16. Декодирование текста
    decoded_sf = sf.decode_text(encoded_sf)
    with open((save_directory_path / 'decoded_shannon_fano.txt').__str__(), 'w', encoding='utf-8') as f:
        f.write(decoded_sf)
    print("Текст декодирован и сохранен в decoded_shannon_fano.txt")
    
    # Проверка корректности
    if decoded_sf == text:
        print("✓ Декодирование выполнено корректно")
    else:
        print("✗ Ошибка декодирования!")
    
    # 17. Двухбуквенные сочетания (Шеннон-Фано)
    print("\n=== МЕТОД ШЕННОНА-ФАНО (ДВУХБУКВЕННЫЕ) ===\n")
    
    bigram_analyzer = BigramAnalyzer(text)
    bigrams = bigram_analyzer.build_bigrams()
    print(f"Построено {len(bigrams)} биграмм")
    
    sf_bigram = ShannonFano(bigram_analyzer.get_frequency_dict())
    sf_bigram.encode()
    sf_bigram.save_to_csv((save_directory_path / 'shannon_fano_bigram.csv').__str__())
    print("Схема кодирования биграмм сохранена в shannon_fano_bigram.csv")
    
    # 18. Метод Хаффмана (однобуквенные)
    print("\n=== МЕТОД ХАФФМАНА (ОДНОБУКВЕННЫЕ) ===\n")
    
    hf = Huffman(analyzer.get_frequency_dict())
    hf.encode()
    hf.save_to_csv((save_directory_path / 'huffman_single.csv').__str__())
    print("Схема кодирования сохранена в huffman_single.csv")
    
    hf_avg_length = hf.calculate_average_length()
    hf_efficiency = hf.calculate_efficiency(entropy)
    
    print(f"Средняя длина кода: {hf_avg_length:.4f} бит/символ")
    print(f"Эффективность сжатия: {hf_efficiency:.2f}%")
    
    # Кодирование и декодирование Хаффманом
    encoded_hf = hf.encode_text(text)
    with open((save_directory_path / 'encoded_huffman.txt').__str__(), 'w') as f:
        f.write(encoded_hf)
    print(f"Текст закодирован ({len(encoded_hf)} бит) и сохранен в encoded_huffman.txt")
    
    decoded_hf = hf.decode_text(encoded_hf)
    with open((save_directory_path / 'decoded_huffman.txt').__str__(), 'w', encoding='utf-8') as f:
        f.write(decoded_hf)
    print("Текст декодирован и сохранен в decoded_huffman.txt")
    
    if decoded_hf == text:
        print("✓ Декодирование выполнено корректно")
    else:
        print("✗ Ошибка декодирования!")
    
    # Метод Хаффмана (двухбуквенные)
    print("\n=== МЕТОД ХАФФМАНА (ДВУХБУКВЕННЫЕ) ===\n")
    
    hf_bigram = Huffman(bigram_analyzer.get_frequency_dict())
    hf_bigram.encode()
    hf_bigram.save_to_csv((save_directory_path / 'huffman_bigram.csv').__str__())
    print("Схема кодирования биграмм сохранена в huffman_bigram.csv")
    
    print("\n=== СРАВНЕНИЕ МЕТОДОВ ===\n")
    print(f"{'Метод':<30} {'Средняя длина':<15} {'Эффективность'}")
    print("-" * 60)
    print(f"{'Шеннон-Фано (одиночные)':<30} {sf_avg_length:<15.4f} {sf_efficiency:.2f}%")
    print(f"{'Хаффман (одиночные)':<30} {hf_avg_length:<15.4f} {hf_efficiency:.2f}%")
    print(f"{'Энтропия':<30} {entropy:<15.4f} {'100.00%'}")
    
    print("\n=== ПРОГРАММА ЗАВЕРШЕНА ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Имя файла для обработки')
    
    args = parser.parse_args()
    main(args)