import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}{Style.BRIGHT}
██████╗ ███████╗███╗   ██╗██╗  ██╗███╗  ██╗ █████╗ ██╗  ██╗██╗  ██╗██╗
██╔══██╗██╔════╝████╗  ██║██║ ██╔╝████╗ ██║██╔══██╗██║ ██╔╝██║ ██╔╝██║
██║  ██║█████╗  ██╔██╗ ██║█████╔╝██╔██╗██║███████║█████╔╝ █████╔╝ ██║
██║  ██║██╔══╝  ██║╚██╗██║██╔═██╗██║╚██╗██║██╔══██║██╔═██╗ ██╔═██╗ ╚═╝
██████╔╝███████╗██║ ╚████║██║  ██║██║ ╚████║██║  ██║██║  ██╗██║  ██╗██╗
╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
{Fore.CYAN}         Stylish Headless Video Looper by RENKAKU
"""

lock = threading.Lock()

def print_status(msg, color=Fore.WHITE):
    with lock:
        print(f"{color}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

def load_proxies(filename):
    try:
        with open(filename, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            raise Exception("No proxies found in the file.")
        return proxies
    except Exception as e:
        print_status(f"[!] Error loading proxies: {e}", Fore.RED)
        sys.exit(1)

def get_user_input():
    url = input(f"{Fore.YELLOW}Enter the video URL to loop: {Style.RESET_ALL}")
    while True:
        try:
            loops = int(input(f"{Fore.YELLOW}How many times do you want to loop the video? {Style.RESET_ALL}"))
            if loops > 0:
                break
            else:
                print_status("Please enter a number greater than 0.", Fore.RED)
        except ValueError:
            print_status("Invalid input. Please enter an integer.", Fore.RED)
    return url, loops

def get_proxy(proxies, loop):
    idx = loop % len(proxies)
    return proxies[idx]

def view_video(url, proxy, loop_num, total_loops):
    thread_id = threading.current_thread().name
    print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Using proxy: {proxy}", Fore.LIGHTBLUE_EX)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-device-discovery-notifications")
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.page_load_strategy = 'eager'

    try:
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Launching headless browser...", Fore.LIGHTGREEN_EX)
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Error launching browser: {e}", Fore.RED)
        return

    try:
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Opening the video link...", Fore.GREEN)
        driver.get(url)
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Viewing for 4 seconds...", Fore.BLUE)
        time.sleep(4)
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Loop complete! Closing browser and switching proxy...\n", Fore.MAGENTA)
    except Exception as e:
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Error during video viewing: {e}", Fore.RED)
    finally:
        driver.quit()
        print_status(f"[{loop_num+1}/{total_loops}][{thread_id}] Browser closed.\n", Fore.LIGHTBLACK_EX)

def main():
    print(BANNER)
    # Use command line args if provided, else prompt interactively
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        loops = int(sys.argv[2])
    else:
        url, loops = get_user_input()

    proxies = load_proxies("working_proxies.txt")
    print_status(f"Loaded {len(proxies)} proxies from working_proxies.txt", Fore.YELLOW)
    print_status(f"Starting headless video looper for: {url}", Fore.CYAN)
    print_status(f"Total loops: {loops}\n", Fore.CYAN)

    max_workers = 5
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(loops):
            proxy = get_proxy(proxies, i)
            futures.append(executor.submit(view_video, url, proxy, i, loops))
        for future in as_completed(futures):
            pass

    print_status(f"All loops finished! Thank you for using RENKAKU's stylish looper.", Fore.LIGHTMAGENTA_EX)

if __name__ == "__main__":
    main()