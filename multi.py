import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = f"""{Fore.RED}
 .----------------.  .----------------.  .-----------------. .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  _______     | || |  _________   | || | ____  _____  | || |  ___  ____   | || |      __      | || |  ___  ____   | || | _____  _____ | |
| | |_   __ \    | || | |_   ___  |  | || ||_   \|_   _| | || | |_  ||_  _|  | || |     /  \     | || | |_  ||_  _|  | || ||_   _||_   _|| |
| |   | |__) |   | || |   | |_  \_|  | || |  |   \ | |   | || |   | |_/ /    | || |    / /\ \    | || |   | |_/ /    | || |  | |    | |  | |
| |   |  __ /    | || |   |  _|  _   | || |  | |\ \| |   | || |   |  __'.    | || |   / ____ \   | || |   |  __'.    | || |  | '    ' |  | |
| |  _| |  \ \_  | || |  _| |___/ |  | || | _| |_\   |_  | || |  _| |  \ \_  | || | _/ /    \ \_ | || |  _| |  \ \_  | || |   \ `--' /   | |
| | |____| |___| | || | |_________|  | || ||_____|\____| | || | |____||____| | || ||____|  |____|| || | |____||____| | || |    `.__.'    | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  
{Style.RESET_ALL}"""
    print(banner)

def main():
    print_banner()

    if len(sys.argv) != 3:
        print(f"{Fore.RED}Usage: python multi.py <video_url> <loops>{Style.RESET_ALL}")
        sys.exit(1)

    url = sys.argv[1]
    try:
        loops = int(sys.argv[2])
        if loops <= 0:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Please provide a valid number of loops (> 0).{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.CYAN}Starting headless video looper for: {url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total loops (refreshes): {loops}{Style.RESET_ALL}\n")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        print(f"{Fore.GREEN}Opening the video link...{Style.RESET_ALL}")
        driver.get(url)
        for i in range(1, loops + 1):
            time.sleep(4)  # 4-second view time
            print(f"{Fore.BLUE}[{i}/{loops}] View done.{Style.RESET_ALL}")
            if i < loops:
                print(f"{Fore.MAGENTA}Refreshing the page...{Style.RESET_ALL}")
                driver.refresh()
        print(f"{Fore.GREEN}All loops (refreshes) finished!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
