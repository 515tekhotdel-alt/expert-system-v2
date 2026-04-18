import requests

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyBmj0da-iaYGxuu5o7Awo8H2f1fi0XLA-T-1tM6DJrRGVyIeQQECLOT-DItLXgJEMJUg/exec"

# Тест 1: GET-запрос (должен вернуть "Script is ready!")
print("Тест 1: GET-запрос")
response = requests.get(SCRIPT_URL)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text}")
print("-" * 40)

# Тест 2: POST-запрос с минимальными данными
print("Тест 2: POST-запрос")
data = {"values": [["test"]]}
response = requests.post(SCRIPT_URL, json=data)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.text[:200]}")
