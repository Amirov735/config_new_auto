import requests
import os
from datetime import datetime

# Твои источники
SOURCES = [
    "https://raw.githubusercontent.com/ewecrow78-gif/whitelist1/main/list.txt",
    "https://raw.githubusercontent.com/ERRORQSFG/fuckwhitelists/refs/heads/main/sub.txt",
    "https://raw.githubusercontent.com/ssavnayt/AWCFG-CONFIG-LIST/refs/heads/main/Configs-AUTO.txt",
    "https://raw.githubusercontent.com/ssavnayt/AWCFG-CONFIG-LIST/refs/heads/main/Configs-all-country.txt",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/refs/heads/main/kizyakbeta6.txt",
    "https://raw.githubusercontent.com/VSd223/vpn/refs/heads/main/vpn",
    "https://airlinkvpn.github.io/1.txt",
    # Добавляй сюда новые источники
]

def is_vless(config: str) -> bool:
    """Проверяем, что это именно VLESS ссылка"""
    cleaned = config.strip()
    return cleaned.startswith("vless://") and len(cleaned) > 10  # минимальная защита от мусора

def fetch_and_merge_vless_only():
    all_vless = []
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            
            # Берём только непустые строки, не начинающиеся с #
            lines = [line.strip() for line in r.text.splitlines() 
                    if line.strip() and not line.strip().startswith('#')]
            
            # Фильтруем только vless
            vless_from_url = [line for line in lines if is_vless(line)]
            
            all_vless.extend(vless_from_url)
            print(f"✅ Получено {len(vless_from_url)} VLESS из {url} (всего строк было: {len(lines)})")
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке {url}: {e}")

    # Убираем дубликаты (сохраняем порядок появления)
    unique_vless = list(dict.fromkeys(all_vless))

    # Дополнительная чистка (на всякий случай)
    unique_vless = [cfg for cfg in unique_vless if is_vless(cfg)]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Основной файл
    with open("NEW_config_v3.txt", "w", encoding="utf-8") as f:
        f.write("# NEW_config_v3 - только VLESS (auto update)\n")
        f.write(f"# Last update: {timestamp}\n")
        f.write(f"# Total VLESS: {len(unique_vless)}\n\n")
        f.write("\n".join(unique_vless) + "\n")

    # Дополнительно можно сохранить в отдельный файл (удобно)
    with open("vless_only.txt", "w", encoding="utf-8") as f:
        f.write("# VLESS only subscription\n")
        f.write(f"# Last update: {timestamp}\n")
        f.write("\n".join(unique_vless) + "\n")

    print(f"✅ Готово! Найдено и сохранено **{len(unique_vless)}** уникальных VLESS конфигов")
    print(f"   → NEW_config_v3.txt")
    print(f"   → vless_only.txt")

if __name__ == "__main__":
    fetch_and_merge_vless_only()
