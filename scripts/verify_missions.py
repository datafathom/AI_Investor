import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_missions_board():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enable console log capture
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        url = "http://127.0.0.1:5173"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Give Vite extra time to bundle/serve
        print("Waiting 15s for app initialization...")
        time.sleep(15) 
        
        print("Injecting login bypass...")
        driver.execute_script("localStorage.setItem('widget_os_bypass', 'true');")
        driver.refresh()
        
        print("Waiting 10s for stability...")
        time.sleep(10)
        
        # Take a health check screenshot
        driver.save_screenshot("screenshots/global_health_check.png")
        print("Screenshot saved: screenshots/global_health_check.png")
        
        # Check for React crash
        source = driver.page_source
        if "Something went wrong" in source:
             print("\n❌ CRITICAL: React Error Boundary still active!")
        else:
             print("\n✅ SUCCESS: App loaded without crash.")
             
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        error_found = False
        for entry in logs:
            level = entry['level']
            message = entry['message']
            print(f"[{level}] {message}")
            if level == 'SEVERE' and "favicon.ico" not in message:
                error_found = True
        
        if error_found:
            print("\n❌ CRITICAL: Severe console errors detected!")
        else:
            print("\n✅ SUCCESS: No severe console errors detected.")
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        try:
            driver.save_screenshot("screenshots/error_final.png")
        except:
            pass
    finally:
        print("\n--- BROWSER CONSOLE LOGS ---")
        try:
            logs = driver.get_log('browser')
            for entry in logs:
                print(f"[{entry['level']}] {entry['message']}")
        except:
            print("Could not retrieve logs.")
        driver.quit()

if __name__ == "__main__":
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    verify_missions_board()
