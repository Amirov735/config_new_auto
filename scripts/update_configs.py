import requests
import datetime
from urllib.parse import urlparse

print("Запуск имбового автообновления конфигов...")

# Читаем источники из sources.txt
with open("sources.txt", "r", encoding="utf-8") as f:
    SOURCES = [line.strip() for line in f if line.strip() and not line.startswith("#")]

all_lines = []
seen = set()

for url in SOURCES:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        lines = response.text.strip().splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line in seen:
                continue
            lower = line.lower()
            # Оставляем vless, vmess, hysteria2 (можно добавить trojan и т.д. если нужно)
            if any(proto in lower for proto in ['vless://', 'vmess://', 'hysteria2://']):
                seen.add(line)
                all_lines.append(line)

        print(f"Собрано из {urlparse(url).netloc}: {len(lines)} строк, после фильтра ~{len(all_lines)}")
    except Exception as e:
        print(f"Пропуск {url}: {e}")

# ... (остальной код остаётся без изменений: header, запись в configs.txt и version.txt)
    
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
