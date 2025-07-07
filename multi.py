import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_user_input():
    url = input("Enter the video URL to loop: ")
    while True:
        try:
            loops = int(input("How many times do you want to loop the video? "))
            if loops > 0:
                break
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    return url, loops

def main():
    url, loops = get_user_input()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--mute-audio")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        for i in range(1, loops + 1):
            time.sleep(4)
            print(i)
            if i < loops:
                driver.refresh()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
