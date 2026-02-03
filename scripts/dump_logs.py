import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def dump_logs():
    print("Dumping Browser Logs...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("http://localhost:5173/analytics/strategy")
        time.sleep(10)
        
        print("\n--- FULL BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        for entry in logs:
            print(f"[{entry['level']}] {entry['message']}")
        print("--- END LOGS ---\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    dump_logs()
