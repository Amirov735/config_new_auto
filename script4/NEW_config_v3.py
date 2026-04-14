import requests
import os
from datetime import datetime

# Твои источники (добавляй новые сюда)
SOURCES = [
    
    "https://airlinkvpn.github.io/1.txt",
    # Добавляй сюда новые источники
]

def is_vless(config: str) -> bool:
    """Жёсткая проверка: ТОЛЬКО VLESS, всё остальное отбрасываем"""
    cleaned = config.strip()
    if not cleaned or cleaned.startswith('#'):
        return False
    # Ищем именно vless:// (регистронезависимо + минимальная длина)
    return cleaned.lower().startswith("vless://") and len(cleaned) > 15

def fetch_and_merge_vless_only():
    all_vless = []
    
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            
            # Берём ВСЕ строки, но сразу отбрасываем пустые и комментарии
            lines = [line.strip() for line in r.text.splitlines() 
                    if line.strip() and not line.strip().startswith('#')]
            
            # 🔥 ЖЁСТКИЙ ФИЛЬТР: оставляем ТОЛЬКО VLESS, всё остальное (vmess, trojan, ss, hysteria и т.д.) — в помойку
            vless_from_url = [line for line in lines if is_vless(line)]
            
            all_vless.extend(vless_from_url)
            print(f"✅ Получено {len(vless_from_url)} VLESS из {url} (всего строк было: {len(lines)})")
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке {url}: {e}")

    # Убираем дубликаты (сохраняем порядок первого появления)
    unique_vless = list(dict.fromkeys(all_vless))

    # Финальная проверка (на всякий случай)
    unique_vless = [cfg for cfg in unique_vless if is_vless(cfg)]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Основной файл
    with open("NEW_config_v3.txt", "w", encoding="utf-8") as f:
        f.write("# NEW_config_v3 - ТОЛЬКО VLESS (auto update)\n")
        f.write(f"# Last update: {timestamp}\n")
        f.write(f"# Total VLESS: {len(unique_vless)}\n")
        f.write("# Все остальные протоколы полностью удалены!\n\n")
        f.write("\n".join(unique_vless) + "\n")

    # Дополнительный чистый файл только VLESS
    with open("vless_only.txt", "w", encoding="utf-8") as f:
        f.write("# VLESS only subscription\n")
        f.write(f"# Last update: {timestamp}\n")
        f.write(f"# Total: {len(unique_vless)}\n\n")
        f.write("\n".join(unique_vless) + "\n")

    print(f"\n🚀 ГОТОВО, БРО!")
    print(f"   Найдено и сохранено **{len(unique_vless)}** уникальных VLESS конфигов")
    print(f"   → NEW_config_v3.txt  (основной)")
    print(f"   → vless_only.txt     (чистый VLESS)")

if __name__ == "__main__":
    fetch_and_merge_vless_only()
