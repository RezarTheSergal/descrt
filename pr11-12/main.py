from rsa import RSA, CRYPTOGRAPHY_AVAILABLE, CryptographyDemo

def main():
    print("="*70)
    print("ПРАКТИКА 11: RSA С САМОПИСНЫМИ ПРИМИТИВАМИ")
    print("="*70)
    
    # Размер ключа
    KEY_BITS = 128  # Для быстрой демонстрации
    
    try:
        # Генерация ключей
        keypair = RSA.generate_keys(KEY_BITS)
        
        print("\n--- Ключи RSA ---")
        print(f"Размер ключа (N): {keypair.n.bit_length()} бит")
        print(f"Модуль N (n = p*q): {hex(keypair.n)[:60]}...")
        print(f"Открытая экспонента E: {keypair.e}")
        print(f"Закрытая экспонента D: {hex(keypair.d)[:60]}...")
        print("-"*70)
        
        # Подготовка текста
        plain_text = "Python RSA Demo!"
        message_bytes = plain_text.encode('utf-8')
        
        print(f"\nИсходное сообщение: '{plain_text}'")
        print(f"Длина сообщения: {len(message_bytes)} байт")
        print("-"*70)
        
        # Шифрование
        print("\n--- Шифрование (M^E mod N, самописное возведение в степень) ---")
        ciphertext = RSA.encrypt(message_bytes, keypair.e, keypair.n)
        print(f"Зашифрованный текст (C): {hex(ciphertext)[:60]}...")
        print("-"*70)
        
        # Дешифрование
        print("\n--- Расшифрование (C^D mod N, самописное возведение в степень) ---")
        decrypted_bytes = RSA.decrypt(ciphertext, keypair.d, keypair.n)
        decrypted_text = decrypted_bytes.decode('utf-8')
        print(f"Расшифрованное сообщение: '{decrypted_text}'")
        print("-"*70)
        
        # Проверка
        if plain_text == decrypted_text:
            print("\nПроверка: Шифрование и расшифрование прошли успешно!")
        else:
            print("\nОшибка: Расшифрованное сообщение не соответствует исходному!")
        
    except Exception as e:
        print(f"\nОшибка: {e}")
    
    print("="*70)
    
    # ПРАКТИКА 12
    print("\n" + "="*70)
    print("ПРАКТИКА 12: ИСПОЛЬЗОВАНИЕ БИБЛИОТЕКИ CRYPTOGRAPHY")
    print("="*70)
    
    try:
        CryptographyDemo.rsa_library_demo()
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()