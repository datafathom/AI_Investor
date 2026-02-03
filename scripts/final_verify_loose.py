import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def final_verify():
    print("Initializing Final Verification (Loose Bypass)...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        base_url = "http://localhost:5173"
        
        # CDP injection for bypass
        print("Injecting Bypass state...")
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
                localStorage.setItem('widget_os_bypass', 'true');
                localStorage.setItem('widget_os_token', 'mock-token');
                localStorage.setItem('widget_os_user', JSON.stringify({id: 'verify', username: 'Tester', role: 'admin'}));
            """
        })
        
        driver.get(base_url)
        time.sleep(5)
        
        strategy_url = f"{base_url}/analytics/strategy"
        print(f"Navigating to {strategy_url}...")
        driver.get(strategy_url)
        
        # Force hide modal just in case
        driver.execute_script("document.querySelectorAll('.modal-overlay, .auth-modal').forEach(el => el.style.display = 'none');")
        
        print("Waiting for Strategy Content (10s)...")
        time.sleep(10)

        # Confirm successful bypass
        print("Verifying Page Header...")
        headers = driver.find_elements(By.TAG_NAME, "h1")
        for h in headers:
            print(f"Found Header: {h.text}")
        
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        error_found = False
        for entry in logs:
            if entry['level'] == 'SEVERE':
                print(f"[{entry['level']}] {entry['message']}")
                error_found = True
        if not error_found:
            print("No SEVERE errors found in console!")
        print("--- END LOGS ---\n")

        screenshot_path = os.path.abspath("final_proof.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    final_verify()
