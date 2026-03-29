import requests
import datetime
import base64
import socket
from urllib.parse import urlparse

# Функция для быстрой проверки: жив ли IP/Порт (TCP чекер)
def is_alive(url_string):
    try:
        # Извлекаем хост и порт для проверки
        parsed = url_string.split('@')[-1].split('?')[0]
        host_port = parsed.split(':')
        host = host_port[0]
        port = int(host_port[1])
        
        with socket.create_connection((host, port), timeout=2):
            return True
    except:
        return False

SOURCES = [
  "https://raw.githubusercontent.com/Amirov735/config_new_auto/refs/heads/main/Promt-bypass.txt",
]

all_lines = []
seen = set()

for url in SOURCES:
    try:
        # Добавляем User-Agent, чтобы гитхаб или источники не банили скрипт
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line in seen:
                continue
            
            # Фильтр протоколов
            if any(proto in line.lower() for proto in ['vless://', 'vmess://', 'hysteria2://']):
                # ХИТРОСТЬ: Проверяем, не забанен ли сервер (опционально, замедляет скрипт)
                # if is_alive(line): 
                seen.add(line)
                all_lines.append(line)
    except Exception as e:
        print(f"Ошибка на {url}: {e}")

# 1. Обычный список (configs_v2.txt)
with open("Promt-bypass.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_lines))

# 2. ХИТРОСТЬ: Base64 версия (для обхода простых фильтров ТСПУ по ключевым словам)
# Назови файл как-нибудь нейтрально, например "data_v2.txt" или "sys_update"
b64_content = base64.b64encode("\n".join(all_lines).encode('utf-8')).decode('utf-8')
with open('Promt-bypass.txt', 'w') as f:
    f.write(your_base64_data)

print(f"Готово! Собрано {len(all_lines)} конфигов.")
