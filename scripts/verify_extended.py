import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def verify_with_extended_wait():
    print("Extended wait verification...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Inject bypass
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
                localStorage.setItem('widget_os_bypass', 'true');
                localStorage.setItem('widget_os_token', 'mock-token');
                localStorage.setItem('widget_os_user', JSON.stringify({id: 'verify', username: 'Tester', role: 'admin'}));
            """
        })
        
        driver.get("http://localhost:5173/analytics/strategy")
        print("Waiting 15s for full page load...")
        time.sleep(15)
        
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        for entry in logs:
            if 'SEVERE' in entry['level'] or 'ERROR' in entry['level'].upper():
                print(f"[{entry['level']}] {entry['message'][:300]}")
        print("--- END LOGS ---\n")
        
        # Check for visible elements
        print("Checking for page content...")
        h1_elements = driver.find_elements(By.TAG_NAME, "h1")
        for h in h1_elements:
            if h.is_displayed():
                print(f"Found H1: {h.text}")
        
        # Check for error boundary messages
        error_divs = driver.find_elements(By.XPATH, "//*[contains(text(), 'Widget Error')]")
        if error_divs:
            print(f"Found {len(error_divs)} error boundary messages")
            for ed in error_divs:
                print(f"  - {ed.text[:100]}")
        else:
            print("No error boundary messages found!")

        screenshot_path = os.path.abspath("strategy_extended.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_with_extended_wait()
