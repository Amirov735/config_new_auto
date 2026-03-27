import requests
import base64
import re
from concurrent.futures import ThreadPoolExecutor

# Список твоих источников
URLS = [
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/good_keys.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/best_keys.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/2.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",
"https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/refs/heads/main/githubmirror/new/by_protocol/hysteria2/hysteria2_001.txt",
"https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    # Сюда можно бахнуть еще 10-20 ссылок, он все переварит
]

def try_decode(content):
    """Безопасное декодирование Base64"""
    content = content.strip()
    if not content: return ""
    if any(prot in content[:100] for prot in ['://']): return content
    try:
        decoded = base64.b64decode(content + "===").decode('utf-8', errors='ignore')
        return decoded if '://' in decoded else content
    except:
        return content

def fetch_url(url):
    """Загрузка и поиск конфигов через регулярки"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) proxy-fetcher'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        data = try_decode(r.text)
        
        # Ищем всё, что похоже на vless, vmess, ss, trojan, hy2, hysteria2, tuic
        pattern = r'(?:vless|vmess|ss|trojan|hysteria2|hy2|tuic)://[^\s|<>"\']+'
        found = re.findall(pattern, data)
        return found
    except Exception as e:
        print(f"[!] Пропуск {url}: {e}")
        return []

def main():
    print("=== START AUTO-UPDATE (6h Cycle) ===")
    
    all_configs = []

    # Качаем всё параллельно (быстро)
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, URLS))

    for res in results:
        all_configs.extend(res)

    # 1. Чистим дубликаты (сохраняем порядок)
    unique_configs = list(dict.fromkeys(all_configs))

    # 2. Убираем явный мусор (слишком короткие строки)
    final_list = [c for c in unique_configs if len(c) > 20]

    # 3. Сохраняем в файл
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))

    print(f"\n[+] Сбор завершен!")
    print(f"[+] Найдено всего: {len(all_configs)}")
    print(f"[+] Уникальных и живых: {len(final_list)}")

if __name__ == "__main__":
    main()
