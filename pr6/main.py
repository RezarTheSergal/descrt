import random
import math
import time
import tracemalloc
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Решето Эратосфена"""
    if limit < 2:
        return []
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(limit + 1) if is_prime[i]]

def gcd(a: int, b: int) -> int:
    """НОД"""
    while b:
        a, b = b, a % b
    return a

def jacobi_symbol(a: int, n: int) -> int:
    """Символ Якоби"""
    if n <= 0 or n % 2 == 0:
        return 0
    
    a %= n
    result = 1
    
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    
    return result if n == 1 else 0

def solovay_strassen_test(p: int, k: int = 20) -> bool:
    """Тест Соловея-Штрассена"""
    if p < 2:
        return False
    if p == 2 or p == 3:
        return True
    if p % 2 == 0:
        return False
    
    for _ in range(k):
        a = random.randint(2, p - 2)
        
        if gcd(a, p) != 1:
            return False
        
        j = pow(a, (p - 1) // 2, p)
        J = jacobi_symbol(a, p)
        J_mod = J % p
        
        if j != J_mod:
            return False
    
    return True

def lehmann_test(p: int, t: int = 20) -> bool:
    """Тест Леманна"""
    if p < 2:
        return False
    if p == 2 or p == 3:
        return True
    if p % 2 == 0:
        return False
    
    one_count = 0
    minus_one_count = 0
    
    for _ in range(t):
        a = random.randint(2, p - 2)
        result = pow(a, (p - 1) // 2, p)
        
        if result != 1 and result != p - 1:
            return False
        
        if result == 1:
            one_count += 1
        if result == p - 1:
            minus_one_count += 1
    
    return one_count > 0 and minus_one_count > 0

def miller_rabin_test(p: int, k: int = 20) -> bool:
    """Тест Рабина-Миллера"""
    if p < 2:
        return False
    if p == 2 or p == 3:
        return True
    if p % 2 == 0:
        return False
    
    b, m = 0, p - 1
    while m % 2 == 0:
        b += 1
        m //= 2
    
    for _ in range(k):
        a = random.randint(2, p - 2)
        z = pow(a, m, p)
        
        if z == 1 or z == p - 1:
            continue
        
        is_composite = True
        for j in range(1, b):
            z = pow(z, 2, p)
            if z == p - 1:
                is_composite = False
                break
            if z == 1:
                return False
        
        if is_composite:
            return False
    
    return True

def trial_division(n: int) -> bool:
    """Пробное деление"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def benchmark_test(test_func, numbers: List[int], iterations: int = 10) -> dict:
    """Бенчмарк теста"""
    tracemalloc.start()
    start_time = time.time()
    
    results = []
    for n in numbers:
        try:
            results.append(test_func(n, iterations))
        except TypeError:
            results.append(test_func(n))
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        'results': results,
        'time': (end_time - start_time) * 1000,
        'memory': peak / 1024
    }

def compare_algorithms(
    base_test_count: int = 100,
    base_max_number: int = 1000,
    base_iterations: int = 10,
    num_runs_per_setting: int = 3  # усреднение по нескольким запускам для стабильности
):
    """Сравнение алгоритмов с построением зависимостей от test_count, max_number, iterations."""
    
    tests = [
        ('Соловей-Штрассен', solovay_strassen_test),
        ('Леманн', lehmann_test),
        ('Рабин-Миллер', miller_rabin_test),
        ('Пробное деление', trial_division)
    ]
    
    # === 1. Зависимость от test_count ===
    test_counts = [100, 250, 500, 750, 1000]
    acc_tc, time_tc, mem_tc = run_parameter_sweep(
        'test_count', test_counts,
        base_test_count, base_max_number, base_iterations,
        tests, num_runs_per_setting
    )

    # === 2. Зависимость от max_number ===
    max_numbers = [100, 1000, 10000, 50000, 100000]
    acc_mn, time_mn, mem_mn = run_parameter_sweep(
        'max_number', max_numbers,
        base_test_count, base_max_number, base_iterations,
        tests, num_runs_per_setting
    )

    # === 3. Зависимость от iterations (только для вероятностных) ===
    iterations_vals = [1, 3, 5, 10, 20, 50]
    acc_it, time_it, mem_it = run_parameter_sweep(
        'iterations', iterations_vals,
        base_test_count, base_max_number, base_iterations,
        tests, num_runs_per_setting
    )

    # === Построение графиков ===
    plot_parameter_dependencies(
        test_counts, acc_tc, time_tc, mem_tc,
        max_numbers, acc_mn, time_mn, mem_mn,
        iterations_vals, acc_it, time_it, mem_it,
        [t[0] for t in tests]
    )

def run_parameter_sweep(param_name, param_values, base_tc, base_mn, base_it, tests, runs):
    """Выполняет серию бенчмарков, варьируя один параметр."""
    accuracy_results = {name: [] for name, _ in tests}
    time_results = {name: [] for name, _ in tests}
    memory_results = {name: [] for name, _ in tests}

    for val in param_values:
        print(f"\nТестируем {param_name} = {val}...")
        
        # Настройка параметров
        if param_name == 'test_count':
            tc, mn, it = val, base_mn, base_it
        elif param_name == 'max_number':
            tc, mn, it = base_tc, val, base_it
        elif param_name == 'iterations':
            tc, mn, it = base_tc, base_mn, val
        else:
            raise ValueError("Неизвестный параметр")

        # Генерация выборки
        test_numbers = [random.randint(2, mn) for _ in range(tc)]
        actual_primes = set(sieve_of_eratosthenes(mn))

        # Усреднение по нескольким запускам
        for name, func in tests:
            acc_sum, time_sum, mem_sum = 0, 0, 0
            for _ in range(runs):
                tracemalloc.start()
                start = time.time()
                try:
                    if name == 'Пробное деление':
                        predictions = [func(n) for n in test_numbers]
                    else:
                        predictions = [func(n, it) for n in test_numbers]
                except Exception as e:
                    print(f"Ошибка в {name} при {param_name}={val}: {e}")
                    predictions = [False] * len(test_numbers)
                end = time.time()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                # Точность
                correct = sum(1 for n, pred in zip(test_numbers, predictions) if pred == (n in actual_primes))
                acc = correct / len(test_numbers) * 100

                acc_sum += acc
                time_sum += (end - start) * 1000
                mem_sum += peak / 1024

            accuracy_results[name].append(acc_sum / runs)
            time_results[name].append(time_sum / runs)
            memory_results[name].append(mem_sum / runs)

    return accuracy_results, time_results, memory_results

def plot_parameter_dependencies(
    test_counts, acc_tc, time_tc, mem_tc,
    max_numbers, acc_mn, time_mn, mem_mn,
    iterations, acc_it, time_it, mem_it,
    names
):
    colors = ["#f83636", "#1dce61", "#090cc5", "#AD108B"]
    
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    params = [
        ('Размер выборки', test_counts, acc_tc, time_tc, mem_tc),
        ('Макс. число', max_numbers, acc_mn, time_mn, mem_mn),
        ('Итерации', iterations, acc_it, time_it, mem_it)
    ]
    
    for col, (title, x_vals, acc, tm, mem) in enumerate(params):
        # Точность
        ax = axes[0, col]
        for i, name in enumerate(names):
            ax.plot(x_vals, acc[name], 'o-', label=name, color=colors[i], linewidth=2)
        ax.set_title(f'Точность vs {title}', fontweight='bold')
        ax.set_xlabel(title)
        ax.set_ylabel('Точность (%)')
        ax.grid(True, alpha=0.3)
        if col == 2:
            ax.legend(fontsize=9)

        # Время
        ax = axes[1, col]
        for i, name in enumerate(names):
            ax.plot(x_vals, tm[name], 's--', label=name, color=colors[i], linewidth=2)
        ax.set_title(f'Время vs {title}', fontweight='bold')
        ax.set_xlabel(title)
        ax.set_ylabel('Время (мс)')
        ax.grid(True, alpha=0.3)

        # Память
        ax = axes[2, col]
        for i, name in enumerate(names):
            ax.plot(x_vals, mem[name], 'd-.', label=name, color=colors[i], linewidth=2)
        ax.set_title(f'Память vs {title}', fontweight='bold')
        ax.set_xlabel(title)
        ax.set_ylabel('Память (КБ)')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('./pr6/prime_tests_parameter_dependency.png', dpi=150, bbox_inches='tight')
    print("\nГрафик зависимостей сохранён: prime_tests_parameter_dependency.png")
    plt.show()

def plot_results(results, primes_256, test_numbers, actual_primes):
    """Построение графиков"""
    
    fig = plt.figure(figsize=(16, 12))
    
    names = [r['name'] for r in results]
    accuracies = [r['accuracy'] for r in results]
    times = [r['time'] for r in results]
    memories = [r['memory'] for r in results]
    
    colors = ["#f83636", "#1dce61", "#090cc5", "#AD108B"]
    
    ax1 = plt.subplot(3, 3, 1)
    bars = ax1.barh(names, accuracies, color=colors)
    ax1.set_xlabel('Точность (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Точность алгоритмов', fontsize=13, fontweight='bold', pad=15)
    ax1.set_xlim(0, 105)
    for i, (bar, acc) in enumerate(zip(bars, accuracies)):
        ax1.text(acc + 1, i, f'{acc:.1f}%', va='center', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    ax2 = plt.subplot(3, 3, 2)
    bars = ax2.bar(names, times, color=colors)
    ax2.set_ylabel('Время (мс)', fontsize=11, fontweight='bold')
    ax2.set_title('Время выполнения', fontsize=13, fontweight='bold', pad=15)
    ax2.tick_params(axis='x', rotation=45)
    for bar, t in zip(bars, times):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{t:.1f}', ha='center', va='bottom', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    ax3 = plt.subplot(3, 3, 3)
    bars = ax3.bar(names, memories, color=colors)
    ax3.set_ylabel('Память (КБ)', fontsize=11, fontweight='bold')
    ax3.set_title('Использование памяти', fontsize=13, fontweight='bold', pad=15)
    ax3.tick_params(axis='x', rotation=45)
    for bar, m in zip(bars, memories):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{m:.1f}', ha='center', va='bottom', fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    ax4 = plt.subplot(3, 3, 4)
    x = np.arange(len(accuracies))
    ax4.plot(x, accuracies, 'o-', color='#4f46e5', linewidth=2, markersize=8)
    ax4.set_xticks(x)
    ax4.set_xticklabels(names, rotation=45, ha='right')
    ax4.set_ylabel('Точность (%)', fontsize=11, fontweight='bold')
    ax4.set_title('Сравнение точности', fontsize=13, fontweight='bold', pad=15)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(min(accuracies) - 5, 105)
    
    ax5 = plt.subplot(3, 3, 5)
    normalized_times = [t / max(times) * 100 for t in times]
    x = np.arange(len(names))
    width = 0.6
    bars = ax5.bar(x, normalized_times, width, color=colors)
    ax5.set_ylabel('Относительное время (%)', fontsize=11, fontweight='bold')
    ax5.set_title('Относительная скорость', fontsize=13, fontweight='bold', pad=15)
    ax5.set_xticks(x)
    ax5.set_xticklabels(names, rotation=45, ha='right')
    ax5.grid(axis='y', alpha=0.3)
    
    ax6 = plt.subplot(3, 3, 6)
    confusion_data = []
    for r in results:
        tp = sum(1 for i, n in enumerate(test_numbers) 
                if r['predictions'][i] and n in actual_primes)
        fp = sum(1 for i, n in enumerate(test_numbers) 
                if r['predictions'][i] and n not in actual_primes)
        fn = sum(1 for i, n in enumerate(test_numbers) 
                if not r['predictions'][i] and n in actual_primes)
        tn = sum(1 for i, n in enumerate(test_numbers) 
                if not r['predictions'][i] and n not in actual_primes)
        confusion_data.append([tp, fp, fn, tn])
    
    categories = ['TP', 'FP', 'FN', 'TN']
    x = np.arange(len(categories))
    width = 0.2
    for i, (r, data) in enumerate(zip(results, confusion_data)):
        ax6.bar(x + i * width, data, width, label=r['name'], color=colors[i])
    ax6.set_ylabel('Количество', fontsize=11, fontweight='bold')
    ax6.set_title('Матрица ошибок', fontsize=13, fontweight='bold', pad=15)
    ax6.set_xticks(x + width * 1.5)
    ax6.set_xticklabels(categories)
    ax6.legend(fontsize=8)
    ax6.grid(axis='y', alpha=0.3)
    
    
    ax9 = plt.subplot(3, 3, 7)
    prime_counts = [len([n for n in test_numbers if n in actual_primes])]
    composite_counts = [len(test_numbers) - prime_counts[0]]
    x = ['Простые', 'Составные']
    bars = ax9.bar(x, [prime_counts[0], composite_counts[0]], 
                   color=['#10b981', '#ef4444'])
    ax9.set_ylabel('Количество', fontsize=11, fontweight='bold')
    ax9.set_title('Распределение в выборке', fontsize=13, fontweight='bold', pad=15)
    for bar in bars:
        height = bar.get_height()
        ax9.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('prime_tests_analysis.png', dpi=150, bbox_inches='tight')
    print("\nГрафик сохранен: prime_tests_analysis.png")
    plt.show()
    
    print(f"\nПростые числа < 256 ({len(primes_256)} чисел):")
    for i in range(0, len(primes_256), 15):
        print("  " + " ".join(f"{p:3d}" for p in primes_256[i:i+15]))
    
    print("\nСводка результатов:")
    for r in results:
        print(f"\n{r['name']}:")
        print(f"  Точность: {r['accuracy']:.2f}%")
        print(f"  Время: {r['time']:.2f} мс")
        print(f"  Память: {r['memory']:.2f} КБ")

if __name__ == "__main__":
    print("Программа тестирования простых чисел")
    print("Анализ зависимостей от параметров\n")
    
    compare_algorithms(
        base_test_count=100,
        base_max_number=1000,
        base_iterations=10,
        num_runs_per_setting=3
    )
    
    print("\nАнализ завершён!")