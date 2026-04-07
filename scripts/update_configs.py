import requests
import base64
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Список источников (можно оставить как есть или читать из sources.txt)
URLS = [
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/good_keys.txt",
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/best_keys.txt",
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/2.txt",
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/refs/heads/main/githubmirror/new/by_protocol/hysteria2/hysteria2_001.txt",
    "https://raw.githubusercontent.com/Kirillo4ka/eavevpn-configs/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/ewecrow78-gif/whitelist1/main/list.txt",
    "https://raw.githubusercontent.com/ERRORQSFG/fuckwhitelists/refs/heads/main/sub.txt",
    "https://raw.githubusercontent.com/ssavnayt/AWCFG-CONFIG-LIST/refs/heads/main/Configs-AUTO.txt",
    "https://raw.githubusercontent.com/ssavnayt/AWCFG-CONFIG-LIST/refs/heads/main/Configs-all-country.txt",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/refs/heads/main/kizyakbeta6.txt",
    "https://raw.githubusercontent.com/VSd223/vpn/refs/heads/main/vpn",
]

def try_decode(content):
    content = content.strip()
    if not content: return ""
    if any(prot in content[:100] for prot in ['://']): return content
    try:
        decoded = base64.b64decode(content + "===").decode('utf-8', errors='ignore')
        return decoded if '://' in decoded else content
    except:
        return content

def fetch_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) proxy-fetcher'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        data = try_decode(r.text)
        pattern = r'(?:vless|vmess|ss|trojan|hysteria2|hy2|tuic)://[^\s|<>"\']+'
        found = re.findall(pattern, data)
        return found
    except Exception as e:
        print(f"[!] Пропуск {url}: {e}")
        return []

def main():
    print("=== START AUTO-UPDATE V3 ===")
    
    all_configs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, URLS))

    for res in results:
        all_configs.extend(res)

    unique_configs = list(dict.fromkeys(all_configs))
    final_list = [c for c in unique_configs if len(c) > 20]

    # === ГЛАВНОЕ ИСПРАВЛЕНИЕ: теперь пишем в NEW_config_v3.txt ===
    with open("NEW_config_v3.txt", "w", encoding="utf-8") as f:
        f.write("# NEW_config_v3.txt - auto update\n")
        f.write(f"# Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total configs: {len(final_list)}\n\n")
        f.write("\n".join(final_list) + "\n")

    print(f"\n[+] Сбор V3 завершен!")
    print(f"[+] Найдено всего: {len(all_configs)}")
    print(f"[+] Уникальных и живых: {len(final_list)}")
    print(f"[+] NEW_config_v3.txt успешно обновлён!")

if __name__ == "__main__":
    main()
