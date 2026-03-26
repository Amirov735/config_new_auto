import requests
import json
from datetime import datetime
import re

# === Настройки ===
WHITELIST_FILE = "WHITELIST.txt"
SOURCES_FILE = "sources.txt"          # создай этот файл со списком ссылок на подписки
BEST_KEYS = "best_keys.txt"
GOOD_KEYS = "good_keys.txt"
SUMMARY_FILE = "summary.json"
CONFIGS_TXT = "configs.txt"           # оставляем для совместимости

def load_whitelist():
    try:
        with open(WHITELIST_FILE, encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("WHITELIST.txt не найден! Создай его.")
        return []

def load_sources():
    try:
        with open(SOURCES_FILE, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except:
        return []

def matches_whitelist(config: str, whitelist: list) -> bool:
    if not whitelist:
        return True
    config_lower = config.lower()
    for domain in whitelist:
        if domain.startswith('*.'):
            base = domain[2:]
            if re.search(rf'[\./]{re.escape(base)}', config_lower):
                return True
        elif domain in config_lower:
            return True
    return False

def main():
    whitelist = load_whitelist()
    sources = load_sources()
    
    print(f"Загружено whitelist доменов: {len(whitelist)}")
    print(f"Источников подписок: {len(sources)}")
    
    all_configs = []
    raw_count = 0
    
    for url in sources:
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            lines = resp.text.splitlines()
            raw_count += len(lines)
            for line in lines:
                line = line.strip()
                if line.startswith(("vless://", "vmess://", "hysteria2://", "tuic://", "trojan://")):
                    all_configs.append(line)
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")
    
    # Убираем дубли
    unique_configs = list(dict.fromkeys(all_configs))
    
    # Фильтруем по whitelist (HardVPN стиль)
    whitelisted = [cfg for cfg in unique_configs if matches_whitelist(cfg, whitelist)]
    
    # Пока простой отбор "best/good" (первые N)
    # Позже добавим реальное тестирование скорости
    best_keys = whitelisted[:100] if len(whitelisted) > 100 else whitelisted
    good_keys = whitelisted[100:500] if len(whitelisted) > 100 else []
    
    # Сохраняем файлы
    with open(BEST_KEYS, "w", encoding="utf-8") as f:
        f.write("\n".join(best_keys))
    
    with open(GOOD_KEYS, "w", encoding="utf-8") as f:
        f.write("\n".join(good_keys))
    
    with open(CONFIGS_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(unique_configs))
    
    # Summary.json как у него
    summary = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sources_processed": len(sources),
        "raw_configs": raw_count,
        "unique_configs": len(unique_configs),
        "whitelisted_configs": len(whitelisted),
        "best_keys": len(best_keys),
        "good_keys": len(good_keys),
        "whitelist_size": len(whitelist),
        "note": "Фильтр по whitelist для России (мобильные белые списки)"
    }
    
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Готово!")
    print(f"   Raw: {raw_count} → Unique: {len(unique_configs)}")
    print(f"   Whitelisted: {len(whitelisted)}")
    print(f"   Best keys: {len(best_keys)} | Good keys: {len(good_keys)}")

if __name__ == "__main__":
    main()
