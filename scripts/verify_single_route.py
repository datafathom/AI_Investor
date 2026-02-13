
import os
import sys
import time
import json
import logging
import urllib.request
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Configuration
FRONTEND_URL = "http://localhost:5173"
BACKEND_URL = "http://localhost:5050"
SCREENSHOT_DIR = Path("docs/_PLANS/Services_Mapped_To_Frontend_Pages/Debug_Screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Test Credentials
TEST_EMAIL = f"route_test_{int(time.time())}@aiinvestor.com"
TEST_PASSWORD = "Password123!"

def api_request(path, method="GET", data=None):
    url = f"{BACKEND_URL}/api/v1{path}"
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
            data_bytes = json.dumps(data).encode('utf-8')
            resp = urllib.request.urlopen(req, data=data_bytes, timeout=10)
        else:
            resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        logger.error(f"API {path} failed: {e}")
        return {"success": False, "detail": str(e)}

def verify_route(route):
    logger.info(f"🚀 Starting verification for: {route}")
    
    # 1. Register fresh user
    logger.info(f"Step 1: Registering {TEST_EMAIL}...")
    reg = api_request("/auth/register", "POST", {"email": TEST_EMAIL, "password": TEST_PASSWORD})
    
    # 2. Verify user
    api_request(f"/auth/verify/{TEST_EMAIL}")
    
    # 3. Selenium Login
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    # Updated way to set logging prefs in newer Selenium/Chrome
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        logger.info("Step 3: Logging in via UI...")
        driver.get(FRONTEND_URL)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))
        
        driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)
        driver.find_element(By.CLASS_NAME, "auth-button").click()
        
        time.sleep(5)
        
        # 4. Navigate to Route
        logger.info(f"Step 4: Navigating to {route}...")
        driver.get(f"{FRONTEND_URL}{route}")
        time.sleep(8) # Extra time for logs to load
        
        # Capture Console Logs
        browser_logs = driver.get_log('browser')
        for log in browser_logs:
            logger.info(f"BROWSER_LOG: {log['level']} - {log['message']}")
            
        page_text = driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"Page content length: {len(page_text)}")
        
        screenshot_path = SCREENSHOT_DIR / f"debug_deep_{route.replace('/', '_')}.png"
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved to: {screenshot_path}")
        
    except Exception as e:
        logger.error(f"Critical error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    route_to_test = sys.argv[1] if len(sys.argv) > 1 else "/admin/logs"
    verify_route(route_to_test)
