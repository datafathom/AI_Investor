import time
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# --- Configuration ---
BASE_URL = "http://localhost:5174"
API_URL = "http://localhost:5050"
SCREENSHOT_DIR = os.path.join("frontend2", "screenshots", "verify_phase_200")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Logger Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    logger.info("Setting up ChromeDriver with Logging...")
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Enable Browser Logging
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def register_and_login(driver):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    email = f"audit_{timestamp}@fathom.ai"
    password = "Password123!"

    logger.info(f"Starting Auth Flow for {email}")
    driver.get(BASE_URL)

    # 1. Register via UI
    try:
        # Wait specifically for the auth-modal to be visible
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "auth-modal")))
        
        # Switch to Register - Try multiple selectors if one fails
        try:
            driver.find_element(By.CLASS_NAME, "switch-auth").click()
        except:
            # Fallback text search
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "Sign Up" in btn.text:
                    btn.click()
                    break
        
        time.sleep(1)

        driver.find_element(By.NAME, "username").send_keys(f"User_{timestamp}") # Might not exist in some versions
        driver.find_element(By.xpath("//input[@type='email']")).send_keys(email)
        driver.find_element(By.xpath("//input[@type='password']")).send_keys(password)
        # Confirm password might not be in all versions, only fill if present
        try:
            driver.find_element(By.NAME, "confirmPassword").send_keys(password)
        except:
            pass
            
        driver.find_element(By.CLASS_NAME, "auth-button").click()
        
        logger.info("Registration submitted via UI")
        time.sleep(3) 

        # Check if we are logged in (App Container visible)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "institutional-os-container")))
            logger.info("Auto-login Successful")
            return
        except:
            logger.info("Auto-login did not happen, trying manual login...")

    except Exception as e:
        logger.error(f"Registration interaction failed: {e}")
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "reg_fail.png"))
        raise

    # 2. Login via UI (Fallback)
    try:
        if len(driver.find_elements(By.CLASS_NAME, "auth-modal")) > 0:
            logger.info("Logging in via UI...")
            driver.find_element(By.xpath("//input[@type='email']")).clear()
            driver.find_element(By.xpath("//input[@type='email']")).send_keys(email)
            driver.find_element(By.xpath("//input[@type='password']")).clear()
            driver.find_element(By.xpath("//input[@type='password']")).send_keys(password)
            driver.find_element(By.CLASS_NAME, "auth-button").click()
    
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "institutional-os-container")))
        logger.info("Login Successful - Dashboard Loaded")

    except Exception as e:
        logger.error(f"Login failed: {e}")
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "login_fail.png"))
        raise

def check_overlap(driver, route_name):
    logger.info(f"Checking for overlaps on {route_name}...")
    widgets = driver.find_elements(By.CLASS_NAME, "glass-panel")
    rects = []
    
    for w in widgets:
        rect = driver.execute_script("return arguments[0].getBoundingClientRect();", w)
        if rect['width'] > 0 and rect['height'] > 0:
            rects.append(rect)

    logger.info(f"Found {len(rects)} visible widgets.")

    overlap_count = 0
    for i, r1 in enumerate(rects):
        for j, r2 in enumerate(rects):
            if i >= j: continue 

            if (r1['left'] < r2['right'] and r1['right'] > r2['left'] and
                r1['top'] < r2['bottom'] and r1['bottom'] > r2['top']):
                
                x_overlap = max(0, min(r1['right'], r2['right']) - max(r1['left'], r2['left']))
                y_overlap = max(0, min(r1['bottom'], r2['bottom']) - max(r1['top'], r2['top']))
                area = x_overlap * y_overlap
                
                if area > 100: 
                    logger.warning(f"Overlap detected between Widget {i} and Widget {j} (Area: {area})")
                    overlap_count += 1

    if overlap_count > 0:
        logger.error(f"FAILED: {overlap_count} overlaps detected on {route_name}")
    else:
        logger.info(f"PASSED: No Layout Overlaps on {route_name}")

def verify_route(driver, route):
    logger.info(f"Verifying Route: {route}")
    driver.get(f"{BASE_URL}{route}")
    
    # Capture Logs
    logs = driver.get_log('browser')
    for log in logs:
        if log['level'] == 'SEVERE':
            logger.error(f"BROWSER ERROR on {route}: {log['message']}")
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "institutional-os-container")))
        time.sleep(3) 
        
        check_overlap(driver, route)
        
        filename = f"VERIFY_{route.replace('/', '_').strip('_')}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        driver.save_screenshot(path)
        logger.info(f"Screenshot saved: {path}")

    except Exception as e:
        logger.error(f"Verification Failed for {route}: {e}")
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, f"FAIL_{route.replace('/', '_').strip('_')}.png"))
        
        # Dump logs again on failure
        logs = driver.get_log('browser')
        for log in logs:
            logger.error(f"Post-Fail Log: {log['message']}")

def main():
    driver = setup_driver()
    try:
        register_and_login(driver)
        
        routes = [
            "/orchestrator",
            "/strategist/scm",
            "/guardian/margin" 
        ]

        for route in routes:
            verify_route(driver, route)
            
    finally:
        driver.quit()
        logger.info("Verification Complete")

if __name__ == "__main__":
    main()
