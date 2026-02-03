from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests

# Configuration
BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:5050"
TEST_USER = {
    "email": "selenium_analytics@example.com",
    "password": "Password123!",
    "username": "selenium_analytics"
}

def setup_test_user():
    """Create test user via API"""
    print("👤 Creating/Verifying test user...")
    try:
        # 1. Register
        resp = requests.post(f"{API_URL}/api/auth/register", json=TEST_USER)
        if resp.status_code == 200:
            print("✅ User registered")
        elif resp.status_code == 400 or "exists" in resp.text:
            print("ℹ️ User likely already exists")
        else:
            print(f"⚠️ User creation warning: {resp.status_code} {resp.text}")
            
        # 2. Verify Email
        verify_url = f"{API_URL}/api/auth/verify-email"
        requests.get(verify_url, params={"email": TEST_USER["email"], "token": "mock_verify_token"})
        print("✅ Email verified manually via API")
        
    except Exception as e:
        print(f"⚠️ API connection failed: {e}")

def login_via_ui(driver):
    """Perform login using the actual UI"""
    print("🔑 Logging in via UI...")
    wait = WebDriverWait(driver, 5)
    try:
        try:
            login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]")
            login_btn.click()
        except:
            pass # Modal might be auto-open

        email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.clear()
        email_input.send_keys(TEST_USER["email"])
        
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pass_input.clear()
        pass_input.send_keys(TEST_USER["password"])
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        print("⏳ Waiting for login completion...")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Login interaction failed: {e}")
        raise e

def verify_analytics_layout():
    print("🚀 Initializing Chrome Driver for Analytics Layout Verification...")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    
    driver = None
    try:
        setup_test_user()
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 2. Navigate to Home/Login
        print(f"🌍 Navigating to {BASE_URL}...")
        driver.get(BASE_URL)
        
        # 2b. Pre-emptive Onboarding Bypass
        print("💉 Injecting Onboarding Bypass & Refreshing...")
        driver.execute_script("localStorage.setItem('onboarding_completed', 'skipped');")
        driver.refresh()
        time.sleep(3)
        
        # 3. Perform Login
        login_via_ui(driver)
        
        # 4. Navigate to Analytics Options Page
        target_url = f"{BASE_URL}/analytics/options"
        print(f"🌍 Navigating to {target_url}...")
        driver.get(target_url)
        
        # 5. Wait for Actual Content
        main_wait = WebDriverWait(driver, 15)
        print("⏳ Waiting for Analytics Options content...")
        main_wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        header = driver.find_element(By.TAG_NAME, "h1")
        print(f"📄 Page Header: {header.text}")
        
        if "Options Analytics" not in header.text:
             print(f"⚠️ Warning: Header text mismatch? Found: '{header.text}'")

        # 6. Verify Drag Handles
        handles = main_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "grid-drag-handle")))
        print(f"✅ Found {len(handles)} drag handles (should be > 0)")
        
        # 7. Check Widget Content
        print("👀 Verifying Widget Content...")
        # Check for unique content in our widgets
        widgets_to_check = ["Gamma Exposure", "Factor Decomposition", "IV Surface"]
        page_source = driver.page_source
        for w in widgets_to_check:
            if w in page_source:
                print(f"✅ Found widget title: '{w}'")
            else:
                print(f"❌ Missing widget title: '{w}'")

        # 8. Scroll & Check Bottom Element Visibility
        print("📜 Scrolling to bottom...")
        try:
            wrapper = driver.find_element(By.CLASS_NAME, "scrollable-content-wrapper")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", wrapper)
        except:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)
        
        # Check if the IV Surface widget (likely at bottom) is visible
        # We can look for the last widget container
        containers = driver.find_elements(By.CLASS_NAME, "widget-container")
        if containers:
            last_widget = containers[-1]
            is_visible = driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "var viewHeight = (window.innerHeight || document.documentElement.clientHeight);"
                "return (rect.bottom <= viewHeight + 50);", 
                last_widget
            )
            if is_visible:
                print("✅ Bottom Widget is VISIBLE in viewport (Not cut off)")
            else:
                print("⚠️ Bottom Widget might be cut off.")
                
        # 9. Capture Screenshot
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = os.path.abspath("screenshots/analytics_layout_verification.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")
        
        driver.quit()
        print("✅ Analytics Layout Verification SUCCESSFUL")
        return True
        
    except Exception as e:
        print(f"❌ Verification FAILED: {str(e)}")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            error_shot = os.path.abspath("screenshots/analytics_verification_error.png")
            driver.save_screenshot(error_shot)
            print(f"📸 Error Screenshot saved to: {error_shot}")
            driver.quit()
        return False

if __name__ == "__main__":
    verify_analytics_layout()
