from typing import Tuple
from gamma import GammaCipher

def main():
    print("=" * 60)
    print("ПРАКТИКА 9: ГАММИРОВАНИЕ")
    print("=" * 60)
    
    # Исходный текст
    plaintext = "Привет, мир! Это секретное сообщение."
    print(f"Открытый текст: {plaintext}")
    
    # Создаём шифр с seed=12345
    cipher = GammaCipher(seed=12345)
    
    # Шифруем
    ciphertext, gamma = cipher.encrypt(plaintext)
    print(f"\nГамма (первые 10 байт): {gamma[:10]}")
    print(f"Зашифрованный текст (hex): {ciphertext.hex()}")
    
    # Дешифруем
    decrypted = cipher.decrypt(ciphertext, gamma)
    print(f"Дешифрованный текст: {decrypted}")
    print(f"Совпадение: {plaintext == decrypted}")

if __name__ == "__main__":
    main()