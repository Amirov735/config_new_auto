import requests
import os
from datetime import datetime

# Твои источники (добавляй сюда новые)
SOURCES = [
    "https://raw.githubusercontent.com/ewecrow78-gif/whitelist1/main/list.txt",
    "https://raw.githubusercontent.com/ERRORQSFG/fuckwhitelists/refs/heads/main/sub.txt",
    "https://raw.githubusercontent.com/ssavnayt/AWCFG-CONFIG-LIST/refs/heads/main/Configs-AUTO.txt",
    "https://raw.githubusercontent.com/ssavnayt/AWCFG-CONFIG-LIST/refs/heads/main/Configs-all-country.txt",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/refs/heads/main/kizyakbeta6.txt",
    "https://raw.githubusercontent.com/VSd223/vpn/refs/heads/main/vpn",  # пример
    # добавь остальные источники как раньше
]

def fetch_and_merge():
    all_configs = []
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            configs = [line.strip() for line in r.text.splitlines() if line.strip() and not line.startswith('#')]
            all_configs.extend(configs)
            print(f"✅ Получено {len(configs)} конфигов из {url}")
        except Exception as e:
            print(f"❌ Ошибка {url}: {e}")

    # Убираем дубли
    unique_configs = list(dict.fromkeys(all_configs))

    # Пишем в новый файл v3
    with open("NEW_config_v3.txt", "w", encoding="utf-8") as f:
        f.write("# NEW_config_v3 - auto update\n")
        f.write(f"# Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n".join(unique_configs) + "\n")

    print(f"✅ NEW_config_v3.txt обновлён! Всего конфигов: {len(unique_configs)}")

if __name__ == "__main__":
    fetch_and_merge()
