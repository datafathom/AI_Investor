import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_redesign():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    try:
        # 1. Login
        print("Navigating to app...")
        driver.get("http://localhost:5173")
        
        # Wait for bypass or login modal
        time.sleep(2)
        
        # Check if login modal is open
        try:
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.send_keys("admin")
            driver.find_element(By.NAME, "password").send_keys("makeMoney")
            driver.find_element(By.CSS_SELECTOR, ".auth-button").click()
            print("Login submitted.")
        except:
            print("Already logged in or bypass active.")
            
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".menu-bar")))
        time.sleep(2) # Wait for animations
        
        # 2. Open Account Dropdown
        # Find the Account menu (it has text "Account" now)
        account_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-item') and contains(text(), 'Account')]")))
        account_menu.click()
        print("Account menu clicked.")
        time.sleep(1)
        
        # 3. Take screenshot of dropdown with username
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots/account_dropdown_v2.png")
        print("Screenshot saved: screenshots/account_dropdown_v2.png")
        
        # 4. Navigate to /account
        # The large button has class .menu-account-profile-item
        profile_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".menu-account-profile-item")))
        profile_btn.click()
        print("Navigating to /account...")
        
        wait.until(EC.url_contains("/account"))
        time.sleep(2) # Wait for staggered animations
        
        # 5. Take screenshot of /account dashboard
        driver.save_screenshot("screenshots/account_dashboard_redesign.png")
        print("Screenshot saved: screenshots/account_dashboard_redesign.png")
        
        # 6. Verify Settings navigation
        account_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-item') and contains(text(), 'Account')]")))
        account_menu.click()
        settings_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-dropdown-item')]//span[contains(text(), 'Settings')]")))
        settings_item.click()
        print("Settings item clicked.")
        
        wait.until(EC.url_contains("/account/settings"))
        print("Successfully navigated to /account/settings.")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")
        driver.save_screenshot("screenshots/verification_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_redesign()
