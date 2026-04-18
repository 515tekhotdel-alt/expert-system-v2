import requests
from datetime import datetime

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw849AwsKvLlqi6e6tbvMwJ7IntMk6JQZ5RHJzAYb-L_idHzkyEFy_GMGd6PiHh-BYqpg/exec"
now = datetime.now()

# Отправляем как form data, а не JSON
data = {
    "date": now.strftime("%d.%m.%Y"),
    "time": now.strftime("%H:%M:%S"),
    "lab": "ТЕСТ",
    "product": "продукт_тест",
    "tnved": "1234",
    "standards": "ГОСТ_ТЕСТ"
}

print(f"📤 Отправляем: {data}")

response = requests.post(SCRIPT_URL, data=data)  # ← data=data, не json!

print(f"📋 Статус: {response.status_code}")
print(f"📋 Ответ: {response.text}")

if response.status_code == 200:
    print("✅ Проверьте таблицу!")