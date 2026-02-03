import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def verify_strategy():
    print("Initializing Selenium verification...")
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
        # Step 1: Login
        base_url = "http://localhost:5173"
        print(f"Navigating to {base_url}...")
        driver.get(base_url)
        time.sleep(5)
        
        print("Checking for login modal...")
        try:
            email_field = driver.find_element("xpath", "//input[contains(@placeholder, 'email') or contains(@placeholder, 'username')]")
            pass_field = driver.find_element("xpath", "//input[@type='password']")
            
            email_field.send_keys("admin@example.com")
            pass_field.send_keys("Admin123!")
            
            login_btn = driver.find_element("xpath", "//button[contains(text(), 'Login') or contains(text(), 'LOGIN')]")
            login_btn.click()
            print("Login submitted.")
            time.sleep(5)
        except Exception as e:
            print(f"Could not find login elements directly. Checking if already logged in or modal is hidden: {e}")

        # Step 2: Navigate to target
        url = f"{base_url}/analytics/strategy"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        print("Waiting for page load and 3D components (10s)...")
        time.sleep(10)
        
        screenshot_path = os.path.abspath("strategy_verification.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        for entry in logs:
            print(f"[{entry['level']}] {entry['message']}")
        print("--- END LOGS ---\n")
        
        # Save page source for debugging if something goes wrong
        with open("strategy_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Save source on error
        try:
            with open("error_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except: pass
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_strategy()
