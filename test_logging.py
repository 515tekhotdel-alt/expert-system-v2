"""
Тест записи в Google Sheets (логирование).
Запускать прямо в PyCharm.
"""

import requests
from datetime import datetime

# ID вашей таблицы
LOG_SHEET_ID = "1xoGoHRLIkS9G7SRSew9XZxh8UQ5_OSwf7-Z7wSRz9e8"


def get_user_ip():
    """Получает IP-адрес."""
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
        return ip
    except Exception as e:
        return f"ошибка: {e}"


def test_write_log():
    """Тестовая запись в таблицу."""
    print("🔄 Тест записи в Google Sheets...")

    # Данные для записи
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M:%S")
    lab = "ТЕСТ"
    product = "тестовый продукт"
    tnved = "0000"
    standards = "ГОСТ ТЕСТ"
    ip = get_user_ip()

    row_data = [[date_str, time_str, lab, product, tnved, standards, ip]]
    print(f"📤 Отправляем: {row_data}")

    # URL для добавления строки
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{LOG_SHEET_ID}/values/A:G:append?valueInputOption=USER_ENTERED"

    headers = {"Content-Type": "application/json"}
    body = {"values": row_data}

    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        print(f"📋 Статус: {response.status_code}")
        print(f"📋 Ответ: {response.text}")

        if response.status_code == 200:
            print("✅ ЗАПИСЬ УСПЕШНА! Проверьте таблицу.")
        else:
            print("❌ ОШИБКА ЗАПИСИ")
    except Exception as e:
        print(f"❌ ИСКЛЮЧЕНИЕ: {e}")


if __name__ == "__main__":
    test_write_log()