"""
Political Alpha Scrolled Screenshot Capture
Navigates to Political Alpha, scrolls to bottom, and captures screenshot
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

BASE_URL = "http://localhost:5173"
SCREENSHOT_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\screenshots\_Debuging"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_political_alpha():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to base for auth
        print("🔐 Authenticating...")
        driver.get(BASE_URL)
        time.sleep(3)
        
        # Auth flow
        today_str = time.strftime("%Y_%m_%d_%H%M%S")
        test_email = f"debug_scroll_{today_str}@datafathom.biz"
        test_pass = "DebugPass123!"
        
        try:
            switch_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "switch-auth")))
            if "Sign Up" in switch_btn.text:
                switch_btn.click()
                time.sleep(1)
            
            email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
            pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            submit_btn = driver.find_element(By.CLASS_NAME, "auth-button")
            
            email_input.send_keys(test_email)
            pass_input.send_keys(test_pass)
            submit_btn.click()
            time.sleep(5)
            
            # Verify email via API
            import requests
            requests.get(f"http://localhost:5050/api/auth/verify-email?email={test_email}&token=mock_verify_token")
            time.sleep(2)
            
            # Refresh and complete login
            driver.get(BASE_URL)
            time.sleep(3)
            
            modals = driver.find_elements(By.CLASS_NAME, "modal-overlay")
            if modals and modals[0].is_displayed():
                email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                submit_btn = driver.find_element(By.CLASS_NAME, "auth-button")
                email_input.clear()
                email_input.send_keys(test_email)
                pass_input.clear()
                pass_input.send_keys(test_pass)
                submit_btn.click()
                time.sleep(3)
                
        except Exception as e:
            print(f"   Auth flow skipped: {e}")
        
        # Skip onboarding
        print("   - Skipping onboarding...")
        driver.execute_script("localStorage.setItem('onboarding_completed', 'skipped');")
        
        # Navigate to Political Alpha
        print("📊 Navigating to Political Alpha...")
        driver.get(f"{BASE_URL}/analytics/political")
        time.sleep(7)  # Wait for full load
        
        # Dismiss any remaining modals
        try:
            modals = driver.find_elements(By.CLASS_NAME, "modal-overlay")
            for modal in modals:
                if modal.is_displayed():
                    # Try clicking outside
                    driver.execute_script("arguments[0].style.display='none';", modal)
        except:
            pass
        time.sleep(2)
        
        # Take initial screenshot
        initial_path = os.path.join(SCREENSHOT_DIR, "PoliticalAlpha_initial.png")
        driver.save_screenshot(initial_path)
        print(f"   ✅ Initial screenshot: {initial_path}")
        
        # Scroll to bottom
        print("📜 Scrolling to bottom...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Take scrolled screenshot
        scrolled_path = os.path.join(SCREENSHOT_DIR, "PoliticalAlpha_scrolled_bottom.png")
        driver.save_screenshot(scrolled_path)
        print(f"   ✅ Scrolled screenshot: {scrolled_path}")
        
        # Check page height
        page_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        scroll_position = driver.execute_script("return window.scrollY")
        
        print(f"\n📏 Page Metrics:")
        print(f"   Total Page Height: {page_height}px")
        print(f"   Viewport Height: {viewport_height}px")
        print(f"   Current Scroll Position: {scroll_position}px")
        print(f"   Max Scroll: {page_height - viewport_height}px")
        
        return scrolled_path
        
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_political_alpha()
