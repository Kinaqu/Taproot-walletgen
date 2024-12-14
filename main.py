import os
from ecdsa import SECP256k1, SigningKey
from hashlib import sha256

# Запрашиваем количество кошельков у пользователя
num_wallets = int(input("Введите количество кошельков для генерации: "))

# Открываем файлы в режиме записи
with open("private.txt", "w") as private_file, open("public.txt", "w") as public_file:
    for i in range(1, num_wallets + 1):
        # Генерируем случайный приватный ключ (32 байта)
        private_key = os.urandom(32)

        # Создаем ключ на основе SECP256k1
        signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
        public_key = signing_key.verifying_key

        # Получаем координаты публичного ключа
        x = public_key.pubkey.point.x()

        # Преобразуем публичный ключ в однокомпонентный формат с использованием x-координаты
        taproot_pubkey = bytes.fromhex(f'{x:064x}')

        # Вычисляем Taproot address (Pay-to-Taproot) используя sha256 от публичного ключа
        taproot_hash = sha256(taproot_pubkey).digest()

        # Добавляем версию адреса для Taproot (0x51), создавая "префикс" P2TR
        taproot_address = "bc1p" + taproot_hash.hex()

        # Проверяем, является ли это последняя итерация
        if i == num_wallets:
            # Записываем без переноса строки в конце
            private_file.write(f"{private_key.hex()}")
            public_file.write(f"{taproot_address}")
        else:
            # Записываем с переносом строки в конце
            private_file.write(f"{private_key.hex()}\n")
            public_file.write(f"{taproot_address}\n")

        print(f"Кошелек {i} успешно сгенерирован!")

print("Генерация всех кошельков завершена! Все приватные ключи сохранены в 'private.txt', а публичные адреса в 'public.txt'.")
