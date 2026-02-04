import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost:5173"
ROUTES_FILE = "notes/All_Frontend_Routes.txt"
SCREENSHOT_DIR = "screenshots/audit"

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Comment out if you want to see the audit
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login(driver):
    print("Logging in...")
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Wait for email input
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        
        email_input.send_keys("admin")
        password_input.send_keys("makeMoney")
        login_button.click()
        
        # Wait for login modal to disappear or dashboard to load
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]")))
        print("Login successful.")
        time.sleep(2)  # Stability wait
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def get_routes():
    routes = []
    if not os.path.exists(ROUTES_FILE):
        print(f"Routes file not found: {ROUTES_FILE}")
        return routes
    
    with open(ROUTES_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                routes.append(line[2:])
    return routes

def audit_route(driver, route):
    url = f"{BASE_URL}{route}"
    print(f"Auditing: {route}")
    driver.get(url)
    
    # Wait 6 seconds as requested
    time.sleep(6)
    
    # Check for console errors
    logs = driver.get_log('browser')
    errors = [log for log in logs if log['level'] == 'SEVERE']
    
    # Capture screenshot
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    safe_name = route.replace('/', '_').strip('_') or 'root'
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
    driver.save_screenshot(screenshot_path)
    
    return {
        "route": route,
        "status": "PASS" if not errors else "FAIL",
        "errors": [log['message'] for log in errors],
        "screenshot": screenshot_path
    }

def main():
    driver = setup_driver()
    results = []
    
    try:
        if not login(driver):
            return
        
        routes = get_routes()
        print(f"Found {len(routes)} routes to audit.")
        
        for route in routes:
            result = audit_route(driver, route)
            results.append(result)
            print(f"Result: {result['status']} ({len(result['errors'])} errors)")
        
        # Save results
        with open("notes/Frontend_Audit_Results.json", "w") as f:
            json.dump(results, f, indent=4)
        
        # Summary
        passes = len([r for r in results if r['status'] == 'PASS'])
        fails = len([r for r in results if r['status'] == 'FAIL'])
        print(f"\nAudit Complete!")
        print(f"Passes: {passes}")
        print(f"Failures: {fails}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
