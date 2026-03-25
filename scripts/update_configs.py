import requests
import datetime
from urllib.parse import urlparse

print("Запуск имбового автообновления конфигов...")

# Список крутых публичных источников (добавляй/убирай свои)
SOURCES = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://gitverse.ru/api/repos/bywarm/rser/raw/branch/master/wl.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt",
]

all_lines = []
seen = set()  # для удаления дублей

for url in SOURCES:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        
        # Фильтруем только нужные протоколы (vless, vmess, hysteria2)
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line in seen:
                continue
            lower = line.lower()
            if any(proto in lower for proto in ['vless://', 'vmess://', 'hysteria2://']):
                seen.add(line)
                all_lines.append(line)
        
        print(f"Собрано из {urlparse(url).netloc}: {len(lines)} строк, после фильтра ~{len(all_lines)}")
    
    except Exception as e:
        print(f"Пропуск {url}: {e}")

# Если ничего не собралось — fallback
if not all_lines:
    all_lines = ["# Нет свежих конфигов — проверь источники"]

# Добавляем красивую шапку и метку
header = f"""# Имбовая коллекция VLESS / VMESS / HYSTERIA2
# Автообновлено: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
# Источники: {len(SOURCES)} подписок | Уникальных: {len(all_lines)}
# Протоколы: vless vmess hysteria2 (фильтр включён)

"""

content = "\n".join(all_lines)

# Добавляем только одну строку в самый конец (для v2rayNG это безопасно)
content += f"\n\n# Auto updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | {len(all_lines)} configs"

# Пишем в configs.txt
with open("configs.txt", "w", encoding="utf-8") as f:
    f.write(header + content)   # ← лучше писать header + content

print(f"Финал: {len(all_lines)} уникальных конфигов сохранено!")

# version.txt для красоты
with open("version.txt", "w", encoding="utf-8") as f:
    f.write(f"Last update: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"Unique configs: {len(all_lines)}\n"
            f"Protocols: vless, vmess, hysteria2")
