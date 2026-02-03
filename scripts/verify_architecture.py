import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def verify_architecture():
    print("Initializing Architectural Verification...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enable console logging
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        base_url = "http://localhost:5173"
        print(f"Navigating to {base_url}...")
        driver.get(base_url)
        time.sleep(5)

        # 1. Test RequestGuard (Blocking direct fetch)
        print("Testing RequestGuard via Console Injection...")
        driver.execute_script("""
            fetch('https://google.com').catch(err => console.error('GUARD_ACTIVE: ' + err.message));
        """)
        time.sleep(2)

        # 2. Check for LocalStorage hydration
        print("Checking LocalStorage for caching/hydration...")
        storage_data = driver.execute_script("return JSON.stringify(localStorage);")
        storage = json.loads(storage_data)
        
        has_cache = any(key.startswith('api_cache_') for key in storage.keys())
        has_brokerage = 'last_brokerage_summary' in storage
        
        print(f"LocalStorage Keys: {list(storage.keys())}")
        print(f"API Cache Found: {has_cache}")
        print(f"Brokerage Summary Persisted: {has_brokerage}")

        # 3. Capture Console Logs for Errors
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        guard_verified = False
        for entry in logs:
            print(f"[{entry['level']}] {entry['message']}")
            if 'GUARD_ACTIVE' in entry['message']:
                guard_verified = True
        print("--- END LOGS ---\n")

        screenshot_path = os.path.abspath("architecture_verification.png")
        driver.save_screenshot(screenshot_path)
        print(f"Verification screenshot saved to {screenshot_path}")

        if guard_verified:
            print("SUCCESS: RequestGuard is actively blocking direct fetches.")
        else:
            print("WARNING: RequestGuard did not report blocking in logs.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_architecture()
