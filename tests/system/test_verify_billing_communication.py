import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def perform_login(driver, base_url):
    print("Performing login as admin...")
    driver.get(f"{base_url}/")
    time.sleep(10)
    
    try:
        # Wait for login modal fields
        wait = WebDriverWait(driver, 30)
        # Select by type since name is missing
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        login_button = driver.find_element(By.CLASS_NAME, "auth-button")
        
        email_input.send_keys("admin@example.com")
        password_input.send_keys("admin")
        login_button.click()
        print("Login button clicked.")
        time.sleep(10)
    except Exception as e:
        print(f"Login failed: {e}")
        driver.save_screenshot("screenshots/login_failure_final.png")

def verify_page(driver, url, page_name):
    print(f"Verifying {page_name} at {url}...")
    try:
        driver.get(url)
        time.sleep(15)  # Significant wait for all widgets
        
        screenshot_path = f"screenshots/verify_{page_name.lower().replace(' ', '_')}.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"Captured screenshot: {screenshot_path} (Size: {os.path.getsize(screenshot_path)} bytes)")
        
        body_text = driver.find_element(By.TAG_NAME, "body").text[:300]
        print(f"Page body preview: {body_text.replace('\n', ' ')}")
    except Exception as e:
        print(f"Error verifying {page_name}: {e}")

def main():
    driver = setup_driver()
    base_url = "http://localhost:5173"
    
    try:
        perform_login(driver, base_url)
        
        # Check current URL to confirm login
        print(f"Current URL after login: {driver.current_url}")
        
        pages = [
            (f"{base_url}/billing/payments", "Bill Payment Dashboard"),
            (f"{base_url}/integrations", "Integrations Dashboard"),
            (f"{base_url}/settings/billing", "Billing Page"),
        ]
        
        for url, name in pages:
            verify_page(driver, url, name)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
