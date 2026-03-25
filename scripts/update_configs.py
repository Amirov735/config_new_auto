import requests
import datetime
from urllib.parse import urlparse

print("Запуск имбового автообновления конфигов...")

# Список крутых публичных источников (добавляй/убирай свои)
SOURCES = [
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",  # твой основной
    "https://raw.githubusercontent.com/prominbro/sub/refs/heads/main/212.txt",
    "https://gist.githubusercontent.com/sevushyamamoto-stack/9341be7a058e132154d407d082a60fb1/raw/mysub.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://mygala.ru/vpn/subscription.txt",
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

49
    50|content = "\n".join(all_lines)
    51|
    52|# Добавляем только одну строку в самый конец (для v2rayNG это безопасно)
    53|content += f"\n\n# Auto updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | {len(all_lines)} configs"
    54|
    55|# Пишем в configs.txt
    56|with open("configs.txt", "w", encoding="utf-8") as f:

# Пишем в configs.txt
with open("configs.txt", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Финал: {len(all_lines)} уникальных конфигов сохранено!")

# version.txt для красоты
with open("version.txt", "w", encoding="utf-8") as f:
    f.write(f"Last update: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"Unique configs: {len(all_lines)}\n"
            f"Protocols: vless, vmess, hysteria2")
