import sys
from hamming_code import HammingCode
from bit_generator import BitGenerator
from error_simulator import ErrorSimulator


def main():
    table_size = int(sys.argv[1])
    combo_size = int(sys.argv[2])
    
    # Проверка корректности параметров
    max_data_bits = 2**table_size - 1 - table_size
    if combo_size > max_data_bits:
        print(f"Максимум {max_data_bits} информационных бит")
        print(f"Вы запросили: {combo_size} бит")
        return
    
    # 1-2.
    original_bits = BitGenerator.generate(combo_size)
    print(f"\nИзначальная комбинация ({combo_size} бит): {original_bits}")
    
    # 3-4.
    hamming = HammingCode(table_size, combo_size)
    print(f"\nПроверочная таблица ({table_size}x{2**table_size - 1}):")
    hamming.print_table()
    
    encoded = hamming.encode(original_bits)
    print(f"\nЗакодированная комбинация ({len(encoded)} бит): {encoded}")
    print(f"Проверочные биты на позициях: {hamming.get_parity_positions()}")
    
    # 5.
    with open('./Output/hamming_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"Исходная комбинация: {original_bits}\n")
        f.write(f"Закодированная: {encoded}\n")
    
    # 6.
    corrupted, error_pos = ErrorSimulator.make_an_error(encoded)
    print(f"\nВнесена ошибка в позицию {error_pos}: {corrupted}")
    
    # 7-8.
    syndrome = hamming.calculate_syndrome(corrupted)
    print(f"\nСиндром ошибки: {syndrome}")
    
    corrected = hamming.correct_error(corrupted, syndrome)
    print(f"\nИсправленная комбинация: {corrected}")

    # 9.
    decoded = hamming.decode(corrected)
    print(f"\nДекодированная комбинация: {decoded}")
    
    print(f"\nИтог:")
    if decoded == original_bits:
        print("Данные полностью восстановлены!")
    else:
        print("Данные не совпадают!")


if __name__ == "__main__":
    main()