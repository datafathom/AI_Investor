
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def prove_terminal_access():
    print("Starting Proof of Access...")
    
    # Setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    BASE_URL = "http://127.0.0.1:5173"
    SCREENSHOT_PATH = os.path.join(os.getcwd(), "screenshots", "proof_terminal_workspace.png")
    os.makedirs(os.path.dirname(SCREENSHOT_PATH), exist_ok=True)

    try:
        # 1. Clear State (Simulate fresh browser)
        driver.get(BASE_URL)
        driver.execute_script("localStorage.clear();")
        driver.refresh()
        print("Cleared local storage.")

        # 2. Login
        print("Navigating to Login...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        
        driver.find_element(By.NAME, "email").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("makeMoney")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Submitted credentials.")

        # 3. Wait for Modal to Vanish
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.NAME, "email")))
        print("Login barrier removed.")

        # 4. Navigate to Terminal
        print("Navigating to Terminal Workspace...")
        driver.get(f"{BASE_URL}/workspace/terminal")
        
        # 5. Wait for specific Terminal element
        # 'terminal-workspace' class or text "System Status"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "terminal-workspace")))
        
        # Verify NO Login Modal
        modals = driver.find_elements(By.NAME, "email")
        if len(modals) > 0 and modals[0].is_displayed():
             print("FATAL: Login modal is still visible!")
        else:
             print("SUCCESS: Login modal is GONE.")

        # 6. Capture Screenshot
        time.sleep(2) # Let animations finish
        driver.save_screenshot(SCREENSHOT_PATH)
        print(f"Proof saved to: {SCREENSHOT_PATH}")

    except Exception as e:
        print(f"FAILED: {e}")
        driver.save_screenshot("failed_proof.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    prove_terminal_access()
