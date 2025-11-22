import os
import sys
import time
from typing import Tuple, List

class XorShiftStarPRNG:
    """Самописный генератор псевдослучайных чисел (XorShift*)"""
    
    def __init__(self, seed: int = None):
        if seed is None:
            seed = int(time.time() * 1000000) & 0xFFFFFFFFFFFFFFFF
        if seed == 0:
            seed = 1  # Состояние не должно быть нулем
        self.state = seed & 0xFFFFFFFFFFFFFFFF
    
    def next_xorshift_star(self) -> int:
        """Генерирует следующее 64-битное число"""
        x = self.state
        x ^= (x >> 12) & 0xFFFFFFFFFFFFFFFF
        x ^= (x << 25) & 0xFFFFFFFFFFFFFFFF
        x ^= (x >> 27) & 0xFFFFFFFFFFFFFFFF
        self.state = x
        return (x * 2685821657736338717) & 0xFFFFFFFFFFFFFFFF
    
    def read_big_int(self, bits: int) -> int:
        """Генерирует случайное большое число заданной длины в битах"""
        result = 0
        num_bytes = (bits + 7) // 8  # Округляем до следующего байта
        
        for i in range(num_bytes):
            r = self.next_xorshift_star()
            byte_val = r & 0xFF
            
            # Сдвигаем результат влево на 8 бит и добавляем новый байт
            result = (result << 8) | byte_val
        
        # Устанавливаем старший бит для требуемой длины
        if bits > 0:
            result |= (1 << (bits - 1))
        
        return result


class PrimeGenerator:
    """Генератор простых чисел с самописным тестом Миллера-Рабина"""
    
    @staticmethod
    def miller_rabin_test(n: int, d: int, s: int, a: int) -> bool:
        """
        Тест Миллера-Рабина для проверки простоты числа
        n-1 = 2^s * d
        """
        x = pow(a, d, n)
        
        n_minus_1 = n - 1
        
        if x == 1 or x == n_minus_1:
            return True
        
        for _ in range(s):
            x = pow(x, 2, n)
            if x == n_minus_1:
                return True
            if x == 1:
                return False
        
        return False
    
    @staticmethod
    def is_probable_prime(n: int) -> bool:
        """Проверка числа на простоту с использованием теста Миллера-Рабина"""

        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        
        # Находим s и d такие, что n - 1 = 2^s * d, где d нечетно
        n_minus_1 = n - 1
        d = n_minus_1
        s = 0
        
        while d % 2 == 0:
            d //= 2
            s += 1
        
        # Детерминированные основания для надежности
        bases = [2, 3, 5, 7, 11]
        
        for a in bases:
            if a >= n:
                continue
            if not PrimeGenerator.miller_rabin_test(n, d, s, a):
                return False
        
        return True
    
    @staticmethod
    def generate_probable_prime(prng: XorShiftStarPRNG, bits: int) -> int:
        """Генерирует простое число заданной битовой длины"""
        while True:
            # Генерируем случайного кандидата
            p = prng.read_big_int(bits)
            
            # Убеждаемся, что число нечетно
            p |= 1
            
            # Проверяем на простоту
            if PrimeGenerator.is_probable_prime(p):
                return p


class ExtendedGCD:
    """Расширенный алгоритм Евклида"""
    
    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Находит x, y такие, что a*x + b*y = gcd(a, b)
        Возвращает: (gcd, x, y)
        """
        r0, r1 = a, b
        x0, x1 = 1, 0
        y0, y1 = 0, 1
        
        while r1 != 0:
            # q = r0 // r1 (частное)
            q = r0 // r1
            
            # r = r0 - q * r1 (новый остаток)
            r = r0 - q * r1
            
            # x = x0 - q * x1
            x = x0 - q * x1
            
            # y = y0 - q * y1
            y = y0 - q * y1
            
            # Обновление переменных
            r0, r1 = r1, r
            x0, x1 = x1, x
            y0, y1 = y1, y
        
        return r0, x0, y0
    
    @staticmethod
    def modular_inverse(a: int, m: int) -> int:
        """Находит обратное по модулю a^-1 mod m"""
        gcd, x, _ = ExtendedGCD.extended_gcd(a, m)
        
        if gcd != 1:
            return None  # Обратного элемента не существует
        
        # Обратный элемент - это x mod m
        return x % m


class ModularExponentiation:
    """Модульное возведение в степень"""
    
    @staticmethod
    def mod_pow(base: int, exponent: int, modulus: int) -> int:
        """
        Модульное возведение в степень (base^exponent mod modulus)
        Алгоритм "Двоичное возведение в степень"
        """
        result = 1
        base = base % modulus
        
        while exponent > 0:
            # Если младший бит экспоненты равен 1
            if exponent & 1:
                result = (result * base) % modulus
            
            # base = base^2 mod modulus
            base = (base * base) % modulus
            
            # exponent = exponent // 2 (сдвиг вправо)
            exponent >>= 1
        
        return result


class RSAKeypair:
    """Пара ключей RSA"""
    
    def __init__(self, n: int, e: int, d: int):
        self.n = n  # Модуль (n = p * q)
        self.e = e  # Открытая экспонента
        self.d = d  # Закрытая экспонента


class RSA:
    """Реализация алгоритма RSA с самописными примитивами"""
    
    @staticmethod
    def generate_primes(bits: int) -> Tuple[int, int]:
        """Генерирует два простых числа"""
        prng = XorShiftStarPRNG(int(time.time() * 1000000))
        
        p = PrimeGenerator.generate_probable_prime(prng, bits)
        q = PrimeGenerator.generate_probable_prime(prng, bits)
        
        return p, q
    
    @staticmethod
    def generate_keys(bits: int) -> RSAKeypair:
        """Генерирует пару ключей RSA"""
        print(f"Генерация простых чисел ({bits} бит)...")
        
        # 1. Сгенерировать два простых числа (p и q)
        p, q = RSA.generate_primes(bits)
        
        print(f"✓ p сгенерировано")
        print(f"✓ q сгенерировано")
        
        # 2. Вычислить модуль n = p * q
        n = p * q
        
        # 3. Вычислить функцию Эйлера phi(n) = (p-1)(q-1)
        phi_n = (p - 1) * (q - 1)
        
        # 4. Выбрать открытую экспоненту e (традиционно 65537)
        e = 65537
        
        # 5. Вычислить закрытую экспоненту d (d = e^-1 mod phi(n))
        d = ExtendedGCD.modular_inverse(e, phi_n)
        
        if d is None:
            raise ValueError("Обратная экспонента d не найдена")
        
        return RSAKeypair(n, e, d)
    
    @staticmethod
    def encrypt(plaintext: bytes, pub_key: int, n: int) -> int:
        """Шифрует сообщение: M^E mod N"""
        # Преобразуем байты в большое число M
        m = int.from_bytes(plaintext, 'big')
        
        # Проверяем, что M < N
        if m >= n:
            raise ValueError("Сообщение слишком длинное для этого RSA, M >= N")
        
        # C = M^E mod N (используем самописное возведение в степень)
        c = ModularExponentiation.mod_pow(m, pub_key, n)
        
        return c
    
    @staticmethod
    def decrypt(ciphertext: int, priv_key: int, n: int) -> bytes:
        """Дешифрует сообщение: C^D mod N"""
        # M = C^D mod N (используем самописное возведение в степень)
        m = ModularExponentiation.mod_pow(ciphertext, priv_key, n)
        
        # Преобразуем большое число M обратно в байты
        num_bytes = (m.bit_length() + 7) // 8
        return m.to_bytes(num_bytes, 'big')


# ==================== ПРАКТИКА 12: ИСПОЛЬЗОВАНИЕ БИБЛИОТЕКИ CRYPTOGRAPHY ====================

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes, padding
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
    
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


class CryptographyDemo:
    """Демонстрация возможностей библиотеки cryptography"""
    
    @staticmethod
    def rsa_library_demo():
        """Демонстрация RSA"""
        print("\n" + "="*70)
        print("RSA Шифрование")
        print("="*70)
        
        print("\n1. Генерация пары ключей RSA:")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        print(f"   Размер ключа: {private_key.key_size} бит")
        
        plaintext = b"Regular secret message for RSA encryption test."
        print(f"\n2. Открытый текст: {plaintext.decode()}")
        
        print(f"\n3. Шифрование:")
        ciphertext = public_key.encrypt(
            plaintext,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"   Зашифрованный текст (hex): {ciphertext.hex()[:60]}...")
        
        print(f"\n4. Дешифрование:")
        decrypted = private_key.decrypt(
            ciphertext,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"   Дешифрованный текст: '{decrypted.decode()}'")
        
        print(f"\n5. Проверка:")
        if plaintext == decrypted:
            print(f"   Тексты совпадают.")