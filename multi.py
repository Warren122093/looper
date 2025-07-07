import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def get_user_input():
    url = input(f"{Fore.YELLOW}Enter the video URL to loop: {Style.RESET_ALL}")
    while True:
        try:
            loops = int(input(f"{Fore.YELLOW}How many times do you want to loop the video? {Style.RESET_ALL}"))
            if loops > 0:
                break
            else:
                print(f"{Fore.RED}Please enter a number greater than 0.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter an integer.{Style.RESET_ALL}")
    return url, loops

def main():
    url, loops = get_user_input()
    print(f"{Fore.CYAN}Starting headless video looper for: {url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total loops: {loops}{Style.RESET_ALL}\n")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--mute-audio")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        for i in range(1, loops + 1):
            print(f"{Fore.GREEN}[{i}/{loops}] Opening the video link...{Style.RESET_ALL}")
            driver.get(url)
            print(f"{Fore.BLUE}  Viewing for 4 seconds...{Style.RESET_ALL}")
            time.sleep(4)
            print(f"{Fore.MAGENTA}  Loop complete! Restarting...{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}All loops finished!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
