import requests

# Ranglar
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
ENDC = '\033[0m'

BANNER = r"""
 __      __          _____      _   _      ______ _           _             
 \ \    / /         |  __ \    | | | |    |  ____(_)         | |            
  \ \  / /__  __  __| |__) |_ _| |_| |__  | |__   _ _ __   __| | ___ _ __  
   \ \/ / _ \ \ \/ /|  ___/ _` | __| '_ \ |  __| | | '_ \ / _` |/ _ \ '__| 
    \  /  __/  >  < | |  | (_| | |_| | | || |    | | | | | (_| |  __/ |    
     \/ \___| /_/\_\|_|   \__,_|\__|_| |_||_|    |_|_| |_|\__,_|\___|_|    
                                                                            
           [ VexPathFinder v1.0 | Python & PHP Hybrid ]
"""

def scan():
    print(CYAN + BANNER + ENDC)
    target = input(f"{GREEN}Target URL (masalan: http://kun.uz): {ENDC}").rstrip('/')
    
    try:
        with open("wordlist.txt", "r") as f:
            paths = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"{RED}[!] wordlist.txt topilmadi!{ENDC}")
        return

    print(f"[*] {len(paths)} ta yo'l tekshirilmoqda...\n")

    for path in paths:
        url = f"{target}/{path}"
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                print(f"{GREEN}[+] TOPILDI: {url} (200 OK){ENDC}")
            elif r.status_code == 403:
                print(f"{RED}[!] TAQIQLANGAN: {url} (403 Forbidden){ENDC}")
        except:
            continue

if __name__ == "__main__":
    scan()
