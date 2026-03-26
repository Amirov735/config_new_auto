import requests
import base64
import re
from concurrent.futures import ThreadPoolExecutor

# Список URL твоих подписок
URLS = [
    "https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/good_keys.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/best_keys.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/2.txt",
"https://raw.githubusercontent.com/ksenkovsolo/HardVPN-bypass-WhiteLists-/refs/heads/main/vpn-lte/subscriptions/1.txt",
"https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
"https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/refs/heads/main/githubmirror/new/by_protocol/hysteria2/hysteria2_001.txt",
    # Добавь сюда остальные свои ссылки
]

def decode_base64(data):
    """Декодирует base64, если данные в нем зашифрованы"""
    try:
        # Убираем лишние пробелы и переходы строк
        data = data.strip().replace('\n', '').replace('\r', '')
        # Добавляем padding, если нужно
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return data # Если не base64, возвращаем как есть

def fetch_url(url):
    """Функция для скачивания данных по одной ссылке"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print(f"[*] Скачиваю: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        content = response.text
        # Проверяем, не base64 ли это (обычно подписки v2ray такие)
        if "://" not in content[:50]: 
            content = decode_base64(content)
            
        return content.splitlines()
    except Exception as e:
        print(f"[!] Ошибка на {url}: {e}")
        return []

def main():
    print("=== Запуск МОЩНОГО обновления конфигов ===")
    
    all_configs = []

    # Запускаем скачивание в 10 потоков одновременно
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_url, URLS)

    for configs in results:
        all_configs.extend(configs)

    # Чистим: убираем пробелы, пустые строки и дубликаты
    clean_configs = []
    for c in all_configs:
        c = c.strip()
        if c and ("://" in c) and (c not in clean_configs):
            clean_configs.append(c)

    # Сохраняем результат
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(clean_configs))

    print(f"\n[+] Готово! Собрано уникальных конфигов: {len(clean_configs)}")
    print("[+] Результат сохранен в configs.txt")

if __name__ == "__main__":
    main()
