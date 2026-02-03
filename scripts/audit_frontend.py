import json
import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Logic
# 1. Start Browser
# 2. Register/Login (Audit Protocol)
# 3. Iterate Pages
# 4. Verify & Screenshot
# 5. Update JSON

BASE_URL = "http://127.0.0.1:5173"
API_URL = "http://127.0.0.1:5050"
NOTES_DIR = os.path.join(os.path.dirname(__file__), "../notes")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "../screenshots")
JSON_PATH = os.path.join(NOTES_DIR, "FrontendPages.json")

def setup_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=1")
    # options.add_argument("--headless") # Comment out for visibility if needed, but user wants screenshots
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_timestamped_email():
    return f"audit_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}@fathom.ai"


def wait_for_backend():
    print("Waiting for Backend to be ready...")
    for i in range(30):
        try:
            requests.get(f"{API_URL}/api/health", timeout=2) # Assuming /api/health exists, or just /
            print("Backend is ready.")
            return True
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nBackend not ready after 30s.")
    return False

def minimize_open_windows(driver):
    try:
        # User requested to minimize all floating widgets (windows) to reveal content
        buttons = driver.find_elements(By.CSS_SELECTOR, ".window-control-minimize")
        clicked_count = 0
        for btn in buttons:
            if btn.is_displayed():
                try:
                    btn.click()
                    clicked_count += 1
                except:
                    pass
        if clicked_count > 0:
            print(f"  -> Minimized {clicked_count} floating windows.")
            time.sleep(1) # Wait for animations
    except Exception as e:
        print(f"  -> Warning: Could not minimize windows: {e}")

def audit_routes():
    # Load Routes
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found.")
        return

    with open(JSON_PATH, "r") as f:
        routes = json.load(f)

    # Prepare Screenshots Directory
    date_str = datetime.now().strftime("%Y-%m-%d")
    today_screenshots_dir = os.path.join(SCREENSHOTS_DIR, date_str)
    os.makedirs(today_screenshots_dir, exist_ok=True)
    
    # 0. Wait for Backend
    if not wait_for_backend():
        print("FATAL: Backend unavailable. Aborting audit.")
        return

    driver = setup_driver()
    
    try:
        # --- Authentication Protocol ---
        print("Starting Authentication Protocol...")
        driver.get(BASE_URL)
        
        # Wait for app to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        
        # Use admin credentials for stability (network/permission robustness)
        email = "admin"
        password = "makeMoney"
        
        print(f"Using admin credentials ({email}) for stability...")
        
        # SKIP REGISTER (Admin hardcoded in backend)
        # SKIP VERIFY (Admin doesn't need verification)
        # print("Verifying user via API...")
        # try:
        #     # Try both paths just in case
        #     r1 = requests.get(f"{API_URL}/api/auth/verify-email?email={email}&token=mock_verify_token")
        #     r2 = requests.get(f"{API_URL}/api/v1/auth/verify-email?email={email}&token=mock_verify_token")
            
        #     if r1.status_code != 200 and r2.status_code != 200:
        #          print("Warning: Verification API returned non-200. Proceeding but Login might fail.")
        # except Exception as e:
        #     print(f"Verification request failed: {e}")

        # LOGIN UI
        print("Logging in via UI...")
        driver.get(BASE_URL + "/login") 
        time.sleep(2)
        
        try:
            email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "email")))
            email_input.clear()
            email_input.send_keys(email)
            
            pass_input = driver.find_element(By.NAME, "password")
            pass_input.clear()
            pass_input.send_keys(password)
            
            # Find submit
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # CRITICAL: Wait for success
            # We assume successful login redirects away or removes the login form
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.NAME, "email")))
            print("Login successful (UI).")
            
        except Exception as e:
            print(f"FATAL: Login UI failed: {e}")
            driver.save_screenshot(os.path.join(today_screenshots_dir, "FATAL_LOGIN_FAIL.png"))
            driver.quit()
            return

        # --- Audit Loop ---
        print("Starting Audit Loop...")
        
        for i, route in enumerate(routes):
            # Refresh routes list each time? No, just iterate.
            url = route.get("pageUrl")
            title = route.get("pageTitle", "Unknown")

            if route.get("status") == "success":
                print(f"Skipping [{i+1}/{len(routes)}]: {title} (Already Success)")
                continue
            
            print(f"Checking [{i+1}/{len(routes)}]: {title} ({url})")
            
            status = "failed"
            try:
                driver.set_page_load_timeout(15)
                driver.get(url)
                
                # Wait for load - User requested at least 3 seconds
                print(f"  -> Waiting 4s for render...")
                time.sleep(4) 
                
                # Check for Browser Console Errors (SEVERE)
                logs = driver.get_log('browser')
                console_errors = [log for log in logs if log['level'] == 'SEVERE']
                
                # Check for Visual UI Errors
                body_text = driver.find_element(By.TAG_NAME, "body").text
                ui_error_indicators = [
                    "Something went wrong",
                    "Minified React error",
                    "Runtime Error",
                    "404 Not Found",
                    "Internal Server Error"
                ]
                found_ui_errors = [err for err in ui_error_indicators if err in body_text]
                
                if "/login" in driver.current_url and "/login" not in url:
                    print(f"  -> FAIL: Redirected to Login.")
                    status = "failed"
                    error_msg = "Redirected to Login"
                elif console_errors:
                    print(f"  -> FAIL: Console Errors detected!")
                    for err in console_errors:
                        print(f"     [CONSOLE] {err['message']}")
                    status = "failed"
                    error_msg = f"Console Error: {console_errors[0]['message'][:50]}..."
                elif found_ui_errors:
                    print(f"  -> FAIL: UI Error Text detected: {found_ui_errors}")
                    status = "failed"
                    error_msg = f"UI Error: {found_ui_errors[0]}"
                else:
                    # Minimize Open Windows before Check/Screenshot
                    minimize_open_windows(driver)
                    status = "success"
                
                # Screenshot
                safe_title = "".join([c if c.isalnum() else "_" for c in title])
                timestamp = datetime.now().strftime('%H%M%S')
                if status == "failed":
                    screenshot_filename = f"FAIL_{safe_title}_{timestamp}.png"
                else:
                    screenshot_filename = f"AUDIT_{safe_title}_{timestamp}.png"
                    
                screenshot_path = os.path.join(today_screenshots_dir, screenshot_filename)
                driver.save_screenshot(screenshot_path)
                
                # Update IN MEMORY & SAVE
                route["status"] = status
                with open(JSON_PATH, "w") as f:
                    json.dump(routes, f, indent=4)

                if status == "failed":
                    print(f"\n[STOPPING] Audit halted due to failure on '{title}'.")
                    print(f"Reason: {error_msg}")
                    print(f"Screenshot: {screenshot_path}")
                    print("Agent: Please fix this error before restarting the audit.")
                    driver.quit()
                    return # Exit function, stop audit

            except Exception as e:
                print(f"  -> Exception Error: {e}")
                status = "failed"
                route["status"] = status
                with open(JSON_PATH, "w") as f:
                    json.dump(routes, f, indent=4)
                print(f"\n[STOPPING] Audit halted due to Exception on '{title}'.")
                driver.quit()
                return # Stop audit

        # Final Write
        print("Updating FrontendPages.json...")
        with open(JSON_PATH, "w") as f:
            json.dump(routes, f, indent=4)
            
    except Exception as e:
         print(f"Fatal Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    audit_routes()
