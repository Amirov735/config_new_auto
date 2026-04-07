import requests
import base64
import re
from concurrent.futures import ThreadPoolExecutor

URLS = [
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
    # Если это уже список ссылок, возвращаем как есть
    if '://' in content[:100]: return content
    try:
        # Пробуем декодировать, если это Base64
        decoded = base64.b64decode(content + "===").decode('utf-8', errors='ignore')
        return decoded
    except:
        return content

def fetch_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        data = try_decode(r.text)
        pattern = r'(?:vless|vmess|ss|trojan|hysteria2|hy2|tuic)://[^\s|<>"\']+'
        return re.findall(pattern, data)
    except Exception as e:
        print(f"[!] Ошибка на {url}: {e}")
        return []

def main():
    all_configs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, URLS))

    for res in results:
        all_configs.extend(res)

    final_list = list(dict.fromkeys([c for c in all_configs if len(c) > 20]))
    
    # Склеиваем всё в одну строку
    out_text = "\n".join(final_list)
    
    # Кодируем в Base64, чтобы клиенты понимали подписку
    encoded_configs = base64.b64encode(out_text.encode('utf-8')).decode('utf-8')

    with open("NEW_config_v3.txt", "w", encoding="utf-8") as f:
        f.write(encoded_configs)

    print(f"Готово! Собрано уникальных: {len(final_list)}")

if __name__ == "__main__":
    main()
