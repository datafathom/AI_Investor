import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_login_enhanced():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = "http://localhost:5173"
        print(f"Opening URL: {url}")
        driver.get(url)
        
        # Wait a bit for initial load
        time.sleep(3)
        
        print("\n--- Page Source Snapshot ---")
        print(driver.page_source[:2000] + "...")
        
        print("\n--- Initial Browser Console Logs ---")
        for entry in driver.get_log('browser'):
            print(f"[{entry['level']}] {entry['message']}")
            
        # Wait for modal
        print("\nWaiting for Login Modal (10s limit)...")
        wait = WebDriverWait(driver, 10)
        try:
            modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "auth-modal")))
            print("Login Modal detected.")
        except Exception as e:
            print(f"TIMEOUT: Modal not detected. {str(e)}")
            driver.save_screenshot("timeout_no_modal.png")
            return

        # Fill credentials
        try:
            email_input = driver.find_element(By.NAME, "email")
            password_input = driver.find_element(By.NAME, "password")
            
            email_input.send_keys("admin")
            password_input.send_keys("makeMoney")
            
            print("Submitting login form...")
            submit_button = driver.find_element(By.CLASS_NAME, "auth-button")
            submit_button.click()
            
            # Wait for "Processing..."
            time.sleep(2)
            print(f"Submit button text: {submit_button.text}")
            
            # Wait for modal to disappear
            print("Waiting for modal to disappear...")
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "auth-modal")))
            print("SUCCESS: Login Modal disappeared.")
            
        except Exception as e:
            print(f"ERROR during interaction: {str(e)}")
            
        print("\n--- Final Browser Console Logs ---")
        for entry in driver.get_log('browser'):
            print(f"[{entry['level']}] {entry['message']}")
            
        driver.save_screenshot("final_state.png")
        print("\nScreenshot saved as final_state.png")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_login_enhanced()
