import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONTEND_URL = "http://localhost:5173"

def test_evolution_ui():
    print("🚀 Starting Evolution Lab UI Log Reaper...")
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Enable Browser Logging
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get(FRONTEND_URL)
        
        # 1. Auth Handling
        try:
             wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "auth-modal")))
             email_in = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
             pass_in = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
             email_in.send_keys("audit@fathom.ai")
             pass_in.send_keys("Password123!")
             btn = driver.find_element(By.CLASS_NAME, "auth-button")
             driver.execute_script("arguments[0].click();", btn)
             wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "auth-modal")))
             print("  [Auth] ✓ Logged in")
        except:
             print("  [Auth] No login required")
        
        # 2. Navigate and Capture Logs
        print(f"  [Action] Navigating to {FRONTEND_URL}/evolution")
        driver.get(f"{FRONTEND_URL}/evolution")
        time.sleep(10) # Heavy wait for 3D/Vite chunks
        
        # Capture Logs
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        for entry in logs:
            print(f"  [{entry['level']}] {entry['message']}")
        print("----------------------------\n")

        # 3. Check for Error Boundary
        if "Something went wrong" in driver.page_source:
             print("❌ Error Boundary detected")
             try:
                 details = driver.find_element(By.TAG_NAME, "summary")
                 driver.execute_script("arguments[0].click();", details)
                 time.sleep(1)
                 error_msg = driver.find_element(By.TAG_NAME, "pre").text
                 print(f"--- STACK TRACE ---\n{error_msg}\n-------------------")
             except Exception as e:
                 print(f"  [Info] Failed to extract stack: {e}")
             raise Exception("Frontend Crash")
        
        # Check Elements
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'EVOLUTION LAB')]")))
        print("✅ Evolution Dashboard Loaded Successfully")

    except Exception as e:
        print(f"❌ UI TEST FAILED: {e}")
        if not os.path.exists("screenshots"): os.makedirs("screenshots")
        driver.save_screenshot("screenshots/LOG_REAPER_CAPTURE.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_evolution_ui()
