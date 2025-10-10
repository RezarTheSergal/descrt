"""
Главный файл программы кодирования Хемминга
Запуск: python main.py <размер_таблицы> <размер_комбинации>
"""
import sys
from hamming_code import HammingCode
from bit_generator import BitGenerator
from error_simulator import ErrorSimulator


def main():
    if len(sys.argv) != 3:
        print("Использование: python main.py <размер_таблицы> <размер_комбинации>")
        print("Пример: python main.py 4 7")
        sys.exit(1)
    
    try:
        table_size = int(sys.argv[1])
        combo_size = int(sys.argv[2])
    except ValueError:
        print("Ошибка: параметры должны быть целыми числами")
        sys.exit(1)
    
    # Проверка корректности параметров
    max_data_bits = 2**table_size - 1 - table_size
    if combo_size > max_data_bits:
        print(f"Ошибка: для таблицы размера {table_size} максимум {max_data_bits} информационных бит")
        print(f"Вы запросили: {combo_size} бит")
        sys.exit(1)
    
    # 1-2. Генерация и вывод комбинации
    print(f"\n{'='*60}")
    print("КОДИРОВАНИЕ ХЕММИНГА")
    print(f"{'='*60}")
    
    generator = BitGenerator()
    original_bits = generator.generate(combo_size)
    print(f"\n1. Исходная комбинация ({combo_size} бит):")
    print(f"   {original_bits}")
    
    # 3-4. Создание таблицы и кодирование
    hamming = HammingCode(table_size, combo_size)
    print(f"\n2. Проверочная таблица ({table_size}x{2**table_size - 1}):")
    hamming.print_table()
    
    encoded = hamming.encode(original_bits)
    print(f"\n3. Закодированная комбинация ({len(encoded)} бит):")
    print(f"   {encoded}")
    print(f"   Проверочные биты на позициях: {hamming.get_parity_positions()}")
    
    # 5. Сохранение результата
    with open('hamming_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"Исходная комбинация: {original_bits}\n")
        f.write(f"Закодированная: {encoded}\n")
    print("\n4. Результат сохранён в 'hamming_result.txt'")
    
    # 6. Внесение ошибки
    error_sim = ErrorSimulator()
    corrupted, error_pos = error_sim.introduce_error(encoded)
    print(f"\n5. Внесена ошибка в позицию {error_pos}:")
    print(f"   {corrupted}")
    
    # 7-8. Поиск и исправление ошибки
    syndrome = hamming.calculate_syndrome(corrupted)
    print(f"\n6. Синдром ошибки: {syndrome} (позиция {syndrome})")
    
    corrected = hamming.correct_error(corrupted, syndrome)
    print(f"\n7. Исправленная комбинация:")
    print(f"   {corrected}")
    
    # 9. Сравнение
    decoded = hamming.decode(corrected)
    print(f"\n8. Декодированная комбинация:")
    print(f"   {decoded}")
    
    print(f"\n{'='*60}")
    if decoded == original_bits:
        print("✓ УСПЕХ! Данные полностью восстановлены")
    else:
        print("✗ ОШИБКА! Данные не совпадают")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()