import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_dashboards():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. Login
        driver.get("http://localhost:5173/login")
        time.sleep(2)
        
        # Check if login modal is open
        try:
            username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Username']")))
            password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Password']")
            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            
            username_input.send_keys("admin")
            password_input.send_keys("makeMoney")
            login_button.click()
            time.sleep(3)
        except:
            print("Already logged in or login failed")

        # 2. Verify Trader Dashboard
        driver.get("http://localhost:5173/trader")
        time.sleep(3)
        driver.save_screenshot("C:/Users/astir/Desktop/AI_Company/AI_Investor/screenshots/trader_dashboard_mission_control.png")
        print("Captured Trader Dashboard")

        # 3. Verify Architect Dashboard
        driver.get("http://localhost:5173/architect")
        time.sleep(3)
        driver.save_screenshot("C:/Users/astir/Desktop/AI_Company/AI_Investor/screenshots/architect_dashboard_mission_control.png")
        print("Captured Architect Dashboard")

        # 4. Verify Account Dashboard
        driver.get("http://localhost:5173/account")
        time.sleep(3)
        driver.save_screenshot("C:/Users/astir/Desktop/AI_Company/AI_Investor/screenshots/account_dashboard_refined.png")
        print("Captured Account Dashboard")

    finally:
        driver.quit()

if __name__ == "__main__":
    if not os.path.exists("C:/Users/astir/Desktop/AI_Company/AI_Investor/screenshots"):
        os.makedirs("C:/Users/astir/Desktop/AI_Company/AI_Investor/screenshots")
    verify_dashboards()
