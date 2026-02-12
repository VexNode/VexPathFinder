import requests
import concurrent.futures
from datetime import datetime
import os

# Ranglar
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[97m'
ENDC = '\033[0m'

BANNER = r"""
 __      __             _____       _   _      ______ _           _             
 \ \    / /            |  __ \     | | | |    |  ____(_)         | |            
  \ \  / /__  __  __   | |__) |__ _| |_| |__  | |__   _ _ __   __| | ___ _ __  
   \ \/ / _ \ \ \/ /   |  ___/ _` | __| '_ \ |  __| | | '_ \ / _` |/ _ \ '__| 
    \  /  __/  >  <    | |  | (_| | |_| | | || |    | | | | | (_| |  __/ |    
     \/ \___| /_/\_\   |_|   \__,_|\__|_| |_||_|    |_|_| |_|\__,_|\___|_|    
                                                                              
           >>> VexPathFinder ULTRA | 87K Wordlist Edition <<<
           >>> Created by: VexNode                          <<<
"""

def request_path(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    try:
        # allow_redirects=False -> qayerga yo'naltirayotganini ko'rish uchun
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
        status = response.status_code
        
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {status} | {url}"
        
        if status == 200:
            msg = f"{GREEN}[200 OK] {url}{ENDC}"
            print(msg)
            save_result(log_entry)
        elif status == 403:
            msg = f"{RED}[403 Forbidden] {url} <-- QIZIQARLI!{ENDC}"
            print(msg)
            save_result(log_entry)
        elif status in [301, 302, 307, 308]:
            redirect_url = response.headers.get('Location', 'Noma\'lum')
            msg = f"{CYAN}[{status} Redirect] {url} -> {redirect_url}{ENDC}"
            print(msg)
            save_result(f"{log_entry} -> {redirect_url}")
            
    except requests.exceptions.RequestException:
        pass

def save_result(data):
    with open("VexResults.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n")

def main():
    print(CYAN + BANNER + ENDC)
    
    target = input(f"{YELLOW}Target URL (masalan: https://google.com): {ENDC}").rstrip('/')
    if not target.startswith('http'):
        target = 'https://' + target

    if not os.path.exists("wordlist.txt"):
        print(f"{RED}[!] wordlist.txt topilmadi!{ENDC}")
        return

    print(f"\n[*] Lug'at yuklanmoqda (87K+ bo'lsa biroz vaqt olishi mumkin)...")
    with open("wordlist.txt", "r", encoding="utf-8", errors="ignore") as f:
        paths = [line.strip() for line in f if line.strip()]

    print(f"[*] Skanerlash boshlandi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] {WHITE}{len(paths)}{ENDC} ta yo'l {GREEN}100 ta tarmoqda{ENDC} tekshirilmoqda...")
    print(f"[*] Natijalar {YELLOW}VexResults.txt{ENDC} fayliga yozilmoqda...\n")

    # Multi-threading: max_workers=100 (87k so'rov uchun ideal tezlik)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        full_urls = [f"{target}/{path.lstrip('/')}" for path in paths]
        executor.map(request_path, full_urls)

    print(f"\n{CYAN}--- Scan Complete. VexNode Out. ---{ENDC}")
    print(f"{GREEN}[!] Natijalarni ko'rish uchun: cat VexResults.txt{ENDC}")

if __name__ == "__main__":
    # Avvalgi natijalarni tozalab tashlash (ixtiyoriy)
    if os.path.exists("VexResults.txt"):
        choice = input(f"{YELLOW}Eski natijalar fayli topildi. Uni o'chirib yangisini ochaymi? (y/n): {ENDC}")
        if choice.lower() == 'y':
            os.remove("VexResults.txt")
            
    main()
