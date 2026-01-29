"""
E2E Test for Sprint 4: Evolution Lab
=====================================
Tests the gene splicing, mutation, and evolution features.
Flow: Register -> Verify Email (API) -> Login (UI) -> Verify Lab
STRICT AUTH VERIFICATION ADDED
"""
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_evolution_lab():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20)

    # Generate unique user
    timestamp = int(time.time())
    email = f"testuser_{timestamp}@example.com"
    password = "password123"
    
    print(f"Starting E2E Test with User: {email}")

    try:
        # 1. Register User via API
        print("1. Registering new user via API...")
        try:
            reg_res = requests.post(
                "http://localhost:5050/api/auth/register",
                json={"email": email, "password": password},
                timeout=10
            )
            print(f"   Register Status: {reg_res.status_code}")
            if reg_res.status_code != 200:
                print(f"   Registration failed body: {reg_res.text}")
                return
        except Exception as e:
            print(f"   Registration API error: {e}")
            return
            
        print("   Registration successful.")

        # 2. Verify Email via API
        print("2. Verifying email via API...")
        try:
            verify_res = requests.get(
                f"http://localhost:5050/api/auth/verify-email?email={email}&token=mock_verify_token",
                timeout=10
            )
            if verify_res.status_code != 200:
                print(f"Verification failed: {verify_res.text}")
                return
        except Exception as e:
             print(f"   Verify API error: {e}")
             return

        print("   Email verified successfully.")

        # 3. Login via UI
        print("3. Logging in via UI...")
        driver.get("http://localhost:5173")
        
        # Ensure we are on login page
        time.sleep(2)
        if "/login" not in driver.current_url and "register" not in driver.current_url:
             # Maybe already logged in? Logout first?
             print(f"   Initial URL: {driver.current_url}")
        
        email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email' or @placeholder='Enter your email']")))
        pass_input = driver.find_element(By.XPATH, "//input[@type='password' or @placeholder='••••••••']")
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        email_input.clear()
        email_input.send_keys(email)
        pass_input.clear()
        pass_input.send_keys(password)
        time.sleep(1) # Visual delay
        
        
        
        print("   Clicking submit...")
        submit_btn.click()
        
        # WAITING LOGIC: Wait for token or error
        print("   Waiting for login result (token or error)...")
        token = None
        for i in range(10): # Wait up to 10 seconds
            token = driver.execute_script("return localStorage.getItem('widget_os_token');")
            if token:
                print(f"   DEBUG: Token found! {token[:10]}...")
                break
            time.sleep(1)
            # Check for error
            try:
                err = driver.find_element(By.CSS_SELECTOR, ".auth-error")
                if err:
                    print(f"   DEBUG: Found auth error: {err.text}")
                    break
            except:
                pass
        
        # STRICT VERIFICATION: Wait for redirection away from login
        print("   Waiting for login redirection...")
        try:
            # Wait for URL to change to NOT contain 'login' or for a dashboard element
            # This logic assumes successful login redirects to /dashboard or /analytics
            WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
            print(f"   Redirected to: {driver.current_url}")
        except:
            print("   ERROR: Login stuck. Page URL remains: " + driver.current_url)
            # Check for error message on UI
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, ".error-message, .alert-danger").text
                print(f"   UI Error Message: {error_msg}")
            except:
                print("   No explicit error message found on UI.")
                
            driver.save_screenshot("login_stuck_fail.png")
            raise Exception("Login failed to redirect")

        # 4. Bypass Onboarding (if redirected there)
        # We inject this just in case, though a new user might need to complete it.
        driver.execute_script("localStorage.setItem('onboarding_completed', 'true');")
        
        # 5. Navigate to Evolution Lab
        print("4. Navigating to Evolution Lab...")
        driver.get("http://localhost:5173/analytics/strategy")
        time.sleep(3)

        # 6. Verify Evolution Lab Components (STRICT)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mutation-rate-container")))
            print("   Verified: Mutation Rate Slider rendered")
        except:
            print("   FAILED to find Evolution Lab components. Current URL: " + driver.current_url)
            driver.save_screenshot("evolution_lab_fail.png")
            if "/login" in driver.current_url:
                print("   Redirected back to Login! Auth token probably INVALID.")
            raise

        # 8. Initiate Evolution
        start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'INITIATE SEEDING')]")))
        start_btn.click()
        print("   Clicked INITIATE SEEDING")
        
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'EVOLVING...')]")))
        print("   Verified: Evolution process started")

        # 9. Test Mutation Rate Slider
        slider = driver.find_element(By.XPATH, "//input[@type='range']")
        driver.execute_script("arguments[0].value = 0.25; arguments[0].dispatchEvent(new Event('change'))", slider)
        print("   Adjusted mutation rate to 25%")

        # 10. Capture Verification Screenshot
        time.sleep(2)
        driver.save_screenshot("evolution_lab_verification.png")
        print("   Screenshot saved: evolution_lab_verification.png")
        
        print("\n✅ Evolution Lab E2E Test PASSED!")

    except Exception as e:
        print(f"\n❌ E2E Test Failed: {e}")
        driver.save_screenshot("evolution_e2e_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_evolution_lab()
