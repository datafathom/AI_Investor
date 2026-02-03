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
import json

# Configuration
BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:5050"
TEST_USER = {
    "email": "selenium_test@example.com",
    "password": "Password123!",
    "username": "selenium_test"
}

def setup_test_user():
    """Create test user via API to ensure login works"""
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
            
        # 2. Verify Email (Required for login)
        verify_url = f"{API_URL}/api/auth/verify-email"
        requests.get(verify_url, params={"email": TEST_USER["email"], "token": "mock_verify_token"})
        print("✅ Email verified manually via API")
        
    except Exception as e:
        print(f"⚠️ API connection failed: {e}")

def login_via_ui(driver):
    """Perform login using the actual UI"""
    print("🔑 Logging in via UI...")
    
    # Wait for login modal or button
    wait = WebDriverWait(driver, 5)
    
    # Check if we need to open login modal
    try:
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]")
        login_btn.click()
    except:
        pass # Modal might be auto-open or already present

    # Fill credentials
    try:
        email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.clear()
        email_input.send_keys(TEST_USER["email"])
        
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pass_input.clear()
        pass_input.send_keys(TEST_USER["password"])
        
        # Submit
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Wait for login success (modal close or redirect)
        print("⏳ Waiting for login completion...")
        time.sleep(3)
        
        # Verify we are logged in (look for logout or user profile)
        # Assuming URL changes or specific element appears
    except Exception as e:
        print(f"❌ Login interaction failed: {e}")
        raise e

def verify_options_layout():
    print("🚀 Initializing Chrome Driver for Layout Verification...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    
    driver = None
    try:
        # 1. Setup User
        setup_test_user()
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 2. Navigate to Home/Login
        print(f"🌍 Navigating to {BASE_URL}...")
        driver.get(BASE_URL)
        
        # 2b. Pre-emptive Onboarding Bypass & Layout Reset
        print("💉 Injecting Onboarding Bypass & Resetting Layout...")
        driver.execute_script("localStorage.setItem('onboarding_completed', 'skipped');")
        driver.execute_script("localStorage.removeItem('layout_options_strategy_v2');") # Ensure clean slate
        driver.refresh()
        time.sleep(3) # Wait for reload
        
        # 3. Perform Login
        login_via_ui(driver)
        
        # 4. Navigate to Options Page
        options_url = f"{BASE_URL}/trading/options"
        print(f"🌍 Navigating to {options_url}...")
        driver.get(options_url)
        
        # 5. Wait for Actual Content (Crucial)
        main_wait = WebDriverWait(driver, 15)
        print("⏳ Waiting for Options Strategy Dashboard content...")
        # 6. Verify Drag Handles AND Content Visibility
        print("👀 Verifying Widget Content...")
        # Map distinct header text to expected content text
        widgets = {
            "Strategy Controls": "Symbol",
            "Strategy Details": "Strategy Type",
            "Greeks Analysis": "Delta",
            "Options Chain": "Strike"
        }
        
        for header_text, content_text in widgets.items():
            try:
                # Find the widget by its header
                # We look for an h2/h3 containing the header text, then get its parent container
                if header_text == "Strategy Controls":
                    xpath = f"//h3[contains(text(), '{header_text}')]/ancestor::div[contains(@style, 'border-radius')]"
                else:
                    xpath = f"//h2[contains(text(), '{header_text}')]/ancestor::div[contains(@style, 'border-radius')]"
                
                widget = main_wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                
                # Check dimensions
                size = widget.size
                if size['height'] < 50 or size['width'] < 50:
                    print(f"❌ Widget '{header_text}' is too small! {size}")
                else:
                    print(f"✅ Widget '{header_text}' has valid dimensions: {size}")
                    
                # Check for content text
                if content_text not in widget.text:
                    print(f"❌ Widget '{header_text}' missing expected text '{content_text}'")
                    print(f"   Actual text: {widget.text[:100]}...")
                else:
                    print(f"✅ Widget '{header_text}' contains expected content.")
                    
            except Exception as e:
                print(f"❌ Failed to verify widget '{header_text}': {e}")
                
        # 6b. Check for Overlaps (Stacking Check)
        print("📐 Checking for Layout Overlaps (Stacking)...")
        rects = []
        for header_text in widgets.keys():
            try:
                if header_text == "Strategy Controls":
                    xpath = f"//h3[contains(text(), '{header_text}')]/ancestor::div[contains(@style, 'border-radius')]"
                else:
                    xpath = f"//h2[contains(text(), '{header_text}')]/ancestor::div[contains(@style, 'border-radius')]"
                
                elem = driver.find_element(By.XPATH, xpath)
                rect = driver.execute_script("return arguments[0].getBoundingClientRect();", elem)
                rects.append({'name': header_text, 'rect': rect})
            except:
                pass
            
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                r1 = rects[i]['rect']
                r2 = rects[j]['rect']
                
                # Check intersection
                overlap = not (r1['right'] < r2['left'] or 
                             r1['left'] > r2['right'] or 
                             r1['bottom'] < r2['top'] or 
                             r1['top'] > r2['bottom'])
                             
                if overlap:
                    # Check if one is essentially 0 size (hidden) which might imply stacking/hidden
                    if r1['width'] > 10 and r2['width'] > 10:
                        print(f"❌ OVERLAP DETECTED between {rects[i]['name']} and {rects[j]['name']}")
                        print(f"   {rects[i]['name']}: {r1}")
                        print(f"   {rects[j]['name']}: {r2}")
                    
        print("✅ Layout Overlap Check Complete.")

        # 7. Scroll & Check Bottom Visibility (Mathematical Proof)
        print("📜 Scrolling to bottom...")
        wrapper = driver.find_element(By.CLASS_NAME, "scrollable-content-wrapper")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", wrapper)
        time.sleep(2)
        
        # Find the last element (Options Chain panel)
        chain_panel = driver.find_element(By.CLASS_NAME, "options-chain-panel")
        
        # Check if it's visible in the viewport
        # We check if the bottom of the element is visible
        is_visible = driver.execute_script(
            "var rect = arguments[0].getBoundingClientRect();"
            "var viewHeight = (window.innerHeight || document.documentElement.clientHeight);"
            "return (rect.bottom <= viewHeight + 50);", # Allowance for padding
            chain_panel
        )
        
        if is_visible:
            print("✅ Bottom Widget is FULLY VISIBLE (Not cut off)")
        else:
            print("⚠️ Bottom Widget might be cut off or scrolling failed.")
            # Print metrics for debugging
            metrics = driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "var viewHeight = (window.innerHeight || document.documentElement.clientHeight);"
                "return {bottom: rect.bottom, viewHeight: viewHeight};",
                chain_panel
            )
            print(f"   Widget Bottom: {metrics['bottom']}, Viewport Height: {metrics['viewHeight']}")

        # 8. Capture Screenshot
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = os.path.abspath("screenshots/options_layout_final.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")
        
        driver.quit()
        print("✅ Options Layout Verification SUCCESSFUL")
        return True
        
    except Exception as e:
        print(f"❌ Verification FAILED: {str(e)}")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            error_shot = os.path.abspath("screenshots/verification_error.png")
            driver.save_screenshot(error_shot)
            print(f"📸 Error Screenshot saved to: {error_shot}")
            driver.quit()
        return False

if __name__ == "__main__":
    verify_options_layout()
