import os
import time
import json
import requests
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
BASE_URL = "http://127.0.0.1:5173"
API_URL = "http://127.0.0.1:5050"
ROUTES_JSON = "notes/All_Frontend_Routes.json"

# Dynamic Storage Configuration
TIMESTAMP = int(time.time())
AUDIT_FOLDER = os.path.join("notes", f"FrontEndAudit_2_3_26")
RESULTS_JSON = os.path.join(AUDIT_FOLDER, f"AuditResults_{TIMESTAMP}.json")
SCREENSHOT_DIR = os.path.join(AUDIT_FOLDER, "screenshots")

# Ensure directories exist
os.makedirs(AUDIT_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# --- User Data ---
TEST_EMAIL = f"audit_{uuid.uuid4().hex[:8]}@example.com"
TEST_PASSWORD = "TestPassword123!"

def setup_driver():
    """Configure and initialize the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Set a global implicit wait just in case
    driver.implicitly_wait(5)
    return driver

def wait_for_backend(url, timeout=30):
    """Wait for the backend to be responsive."""
    print(f"Waiting for backend at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print("Backend is ready.")
                return True
        except:
            pass
        time.sleep(1)
        print(".", end="", flush=True)
    print("\nBackend wait timed out.")
    return False

def register_and_verify():
    """Registers a new user via API and verifies them."""
    print(f"--- Registration Protocol ---")
    
    # Wait for backend warmup
    if not wait_for_backend(f"{API_URL}/health"):
        # Try without /health if it doesn't exist
        if not wait_for_backend(f"{API_URL}/"):
             return False

    print(f"Registering user: {TEST_EMAIL}")
    
    # 1. Register
    reg_url = f"{API_URL}/api/v1/auth/register"
    reg_payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    
    try:
        response = requests.post(reg_url, json=reg_payload, timeout=10)
        if response.status_code not in [200, 201]:
            print(f"Registration failed: {response.status_code} - {response.text}")
            return False
        print("Registration successful.")
    except Exception as e:
        print(f"Registration request error: {e}")
        return False
    
    # 2. Verify
    print("Verifying email...")
    verify_url = f"{API_URL}/api/v1/auth/verify-email"
    verify_params = {"email": TEST_EMAIL, "token": "mock_verify_token"}
    
    try:
        response = requests.get(verify_url, params=verify_params, timeout=10)
        if response.status_code != 200:
            print(f"Verification failed: {response.status_code} - {response.text}")
            return False
        print("Email verification successful.")
    except Exception as e:
        print(f"Verification request error: {e}")
        return False
    
    return True

def login(driver):
    """Log in via the UI and ensure the login modal is gone."""
    print(f"--- Login Protocol ---")
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    
    try:
        # Wait for the login modal/form
        print("Waiting for login email input...")
        email_input = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
        pass_input = driver.find_element(By.NAME, "password")
        
        # Try both common selectors for the button
        try:
            submit_btn = driver.find_element(By.CLASS_NAME, "auth-button")
        except:
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
        print(f"Submitting login for {TEST_EMAIL}...")
        email_input.clear()
        email_input.send_keys(TEST_EMAIL)
        pass_input.clear()
        pass_input.send_keys(TEST_PASSWORD)
        submit_btn.click()
        
        # Wait for modal to disappear
        print("Waiting for auth-modal to disappear...")
        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "auth-modal")))
        except:
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]")))
        
        # Additional wait for stability
        time.sleep(10)
        
        # Double check we aren't on login page anymore
        if "/login" in driver.current_url.lower():
            print(f"Warning: Still on {driver.current_url}")
            return False
            
        print("Login successful and confirmed.")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        # Capture failure screenshot
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "login_failure.png"))
        return False

def audit_routes(driver):
    """Iterate through all routes and audit them."""
    print(f"--- Starting Frontend Audit ---")
    
    if not os.path.exists(ROUTES_JSON):
        print(f"Error: {ROUTES_JSON} not found.")
        return []

    with open(ROUTES_JSON, 'r') as f:
        data = json.load(f)
        routes = data.get("routes", [])

    # Load existing results if they exist to support resuming
    results = []
    if os.path.exists(RESULTS_JSON):
        try:
            with open(RESULTS_JSON, 'r') as f:
                results = json.load(f)
            print(f"Resuming from existing results file ({len(results)} audited).")
        except:
            results = []

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    # Create a map of already audited routes for faster lookup
    audited_paths = {r["route_url"]: r for r in results}

    for i, route_data in enumerate(routes):
        path = route_data.get("path")
        description = route_data.get("description", "No description")
        
        # Skip if already audited and successful
        if path in audited_paths and audited_paths[path]["status"] == "Success":
            print(f"[{i+1}/{len(routes)}] Skipping already successful: {path}")
            continue

        print(f"[{i+1}/{len(routes)}] Auditing: {path} ({description})")
        
        url = f"{BASE_URL}{path}"
        start_time = time.time()
        
        result = {
            "route_title": description,
            "route_url": path,
            "page_load_time": 0,
            "status": "Pending",
            "fail_reason": None
        }
        
        try:
            status = "Success"
            fail_reason = None

            # Check if driver is still alive
            try:
                _ = driver.window_handles
            except:
                print("  -> Driver lost. Re-establishing...")
                driver = setup_driver()
                if not login(driver):
                    print("  -> Could not re-log in. Aborting loop.")
                    break

            # Set timeouts
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(60)
            
            driver.get(url)
            
            # Wait for main container or specific indicators
            time.sleep(5) 
            
            # Capture console logs
            logs = driver.get_log('browser')
            found_console_errors = [l['message'] for l in logs if l['level'] in ['SEVERE', 'ERROR']]
            
            # Check for crash indicator
            page_source = driver.page_source.lower()
            found_ui_errors = []
            if "something went wrong" in page_source:
                found_ui_errors.append("Crash screen detected")
            if "error" in page_source and "not found" in page_source:
                found_ui_errors.append("404-like text in page")

            # Measure load time
            load_time = time.time() - start_time
            result["page_load_time"] = round(load_time, 2)
            
            if found_console_errors:
                status = "Failed"
                # Truncate for display
                err_msg = " ; ".join(found_console_errors)[:200]
                fail_reason = f"Console Errors: {err_msg}"
            elif found_ui_errors:
                status = "Failed"
                fail_reason = f"UI Errors: {'; '.join(found_ui_errors)}"
            elif "/login" in driver.current_url and path != "/login":
                status = "Failed"
                fail_reason = "Redirected to Login"
            
            # Save screenshot for audit evidence (regardless of status)
            # Sanitize description for filename
            safe_name = description.lower().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '').replace('.', '_')
            if not safe_name: # Fallback for empty description
                safe_name = path.replace("/", "_").strip("_") or "root"

            screenshot_name = f"{safe_name}.png"
            if status == "Failed":
                screenshot_name = f"FAIL_{screenshot_name}"
            
            screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
            driver.save_screenshot(screenshot_path)
            
            result["status"] = status
            result["fail_reason"] = fail_reason

            if status == "Failed":
                print(f"  -> Failed: {result['fail_reason']}")
            
        except Exception as e:
            result["status"] = "Failed"
            result["fail_reason"] = str(e)[:200]
            print(f"  -> Exception: {e}")
            
        # Update results list
        if path in audited_paths:
            # Replace old entry
            for idx, r in enumerate(results):
                if r["route_url"] == path:
                    results[idx] = result
                    break
        else:
            results.append(result)
            audited_paths[path] = result
            
        # Save progress every route now for safety
        with open(RESULTS_JSON, 'w') as f:
            json.dump(results, f, indent=4)

    return results


def main():
    if not register_and_verify():
        print("Aborting: Could not register/verify user.")
        return

    driver = setup_driver()
    try:
        if not login(driver):
            print("Aborting: Login failed.")
            return

        results = audit_routes(driver)
        
        success_count = len([r for r in results if r["status"] == "Success"])
        fail_count = len([r for r in results if r["status"] == "Failed"])
        
        print("\n--- Audit Summary ---")
        print(f"Total Routes: {len(results)}")
        print(f"Success: {success_count}")
        print(f"Failed: {fail_count}")
        print(f"Results saved to: {RESULTS_JSON}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
