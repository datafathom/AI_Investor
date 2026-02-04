import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5173"
ROUTES_FILE = "notes/All_Frontend_Routes.txt"
SCREENSHOT_DIR = "screenshots/final_audit"

import requests

def wait_for_runtimes(backend_url="http://127.0.0.1:5050/health", frontend_url="http://127.0.0.1:5173", timeout=60):
    print(f"Waiting for runtimes (Backend: {backend_url}, Frontend: {frontend_url})...")
    start_time = time.time()
    backend_up = False
    frontend_up = False
    
    while time.time() - start_time < timeout:
        if not backend_up:
            try:
                response = requests.get(backend_url, timeout=2)
                if response.status_code == 200:
                    print("Backend is healthy!")
                    backend_up = True
            except: pass
            
        if not frontend_up:
            try:
                # Use a simple socket check or requests for frontend
                response = requests.get(frontend_url, timeout=2)
                if response.status_code == 200 or response.status_code == 404: # Vite index might be 404 if not ready but port is open
                    print("Frontend port is listening!")
                    frontend_up = True
            except: pass
            
        if backend_up and frontend_up:
            return True
        time.sleep(2)
        
    print(f"Timed out. Backend Up: {backend_up}, Frontend Up: {frontend_up}")
    return False

def setup_driver():
    # Ensure runtimes are up before even starting the driver
    wait_for_runtimes()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver):
    print(f"Opening {BASE_URL}...")
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)
    
    try:
        # Wait for login modal
        print("Waiting for login modal...")
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        # Find button that contains 'Login' text
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        
        print("Entering credentials...")
        email_input.send_keys("admin")
        password_input.send_keys("makeMoney")
        login_button.click()
        
        # Wait for modal to disappear
        print("Waiting for login to complete...")
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "auth-modal")))
        # Wait for dashboard content
        time.sleep(3)
        print("Login successful.")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        driver.save_screenshot("login_failed.png")
        return False

def get_routes():
    routes = []
    if not os.path.exists(ROUTES_FILE):
        print(f"Routes file not found: {ROUTES_FILE}")
        # Default fallback routes if file missing
        return ["/dashboard", "/assets", "/portfolio/cash-flow", "/portfolio/crypto", "/strategist/estate", "/evolution"]
    
    with open(ROUTES_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                routes.append(line[2:])
            elif line.startswith("/"):
                routes.append(line)
    return sorted(list(set(routes)))

def audit_route(driver, route):
    url = f"{BASE_URL}{route}"
    print(f"\nAuditing: {route}")
    driver.get(url)
    
    # Wait for page load and any async components
    time.sleep(10)
    
    # Check for console logs
    logs = driver.get_log('browser')
    errors = [log['message'] for log in logs if log['level'] in ['SEVERE', 'ERROR']]
    warnings = [log['message'] for log in logs if log['level'] == 'WARNING']
    
    # Check for Login Modal visibility
    modal_visible = False
    try:
        modals = driver.find_elements(By.CLASS_NAME, "auth-modal")
        for modal in modals:
            if modal.is_displayed():
                modal_visible = True
                break
    except:
        pass

    # Check for "Login Required" text
    login_text_found = "Login" in driver.page_source and ("required" in driver.page_source.lower() or "please" in driver.page_source.lower())
    
    # Capture screenshot
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    safe_name = route.replace('/', '_').strip('_') or 'root'
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
    driver.save_screenshot(screenshot_path)
    
    status = "PASS"
    if errors or modal_visible:
        status = "FAIL"
    
    return {
        "route": route,
        "status": status,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "modal_visible": modal_visible,
        "screenshot": screenshot_path
    }

def main():
    driver = setup_driver()
    results_file = "notes/Frontend_Audit_Results.json"
    
    # Load existing results to skip PASSING routes
    existing_results = {}
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
                # Handle both list and dict formats if they vary
                if isinstance(data, list):
                    existing_results = {r['route']: r for r in data}
                else:
                    existing_results = data
        except Exception as e:
            print(f"Warning: Could not load existing results: {e}")

    try:
        if not login(driver):
            print("Aborting audit due to login failure.")
            return
        
        all_routes = get_routes()
        # Filter routes: Only audit if not in existing_results or status is not PASS
        routes_to_audit = [r for r in all_routes if r not in existing_results or existing_results[r].get('status') != 'PASS']
        
        print(f"Total routes found: {len(all_routes)}")
        print(f"Already passing: {len(all_routes) - len(routes_to_audit)}")
        print(f"Routes to audit (FAIL or NEW): {len(routes_to_audit)}")
        
        if not routes_to_audit:
            print("\n✅ All routes are already passing. Nothing to audit.")
            return

        for route in routes_to_audit:
            result = audit_route(driver, route)
            existing_results[route] = result
            print(f"Result: {result['status']} | E: {result['error_count']} | W: {result['warning_count']} | Modal: {result['modal_visible']}")
            if result['errors']:
                print("  ERRORS:")
                for e in result['errors']:
                    print(f"    - {e}")
        
        # Save merged results
        final_list = list(existing_results.values())
        with open(results_file, "w") as f:
            json.dump(final_list, f, indent=4)
        
        # Summary report
        passes = len([r for r in final_list if r['status'] == 'PASS'])
        fails = len([r for r in final_list if r['status'] == 'FAIL'])
        
        print("\n" + "="*50)
        print("AUDIT OVERALL RESULTS")
        print("="*50)
        print(f"Total Routes in System: {len(final_list)}")
        print(f"Passes: {passes}")
        print(f"Failures: {fails}")
        print("="*50)
        
        if fails > 0:
            print("\nFailing Routes Highlights:")
            for r in final_list:
                if r['status'] == 'FAIL':
                    print(f"- {r['route']}: E:{r['error_count']}, W:{r['warning_count']}, Modal:{r['modal_visible']}")
        print(f"\nDetailed results saved to {results_file}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
