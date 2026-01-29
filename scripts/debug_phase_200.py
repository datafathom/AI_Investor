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

# --- Configuration ---
BASE_URL = "http://localhost:5174"
SCREENSHOT_DIR = os.path.join("frontend2", "screenshots", "debug_phase_200")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def dump_logs(driver, context=""):
    logger.info(f"--- Browser Logs ({context}) ---")
    for log in driver.get_log('browser'):
        logger.error(f"[{log['level']}] {log['message']}")
    logger.info("-----------------------------")

def main():
    driver = setup_driver()
    try:
        logger.info(f"Navigating to {BASE_URL}...")
        driver.get(BASE_URL)
        time.sleep(2)
        dump_logs(driver, "Initial Load")

        # Check for crash (empty body or error boundary)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if not body_text or "Error" in body_text:
            logger.error(f"Possible App Crash. Body text: {body_text[:200]}")
        
        # Try to find Auth Modal
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "auth-modal")))
            logger.info("Auth Modal Found - App is Interactive")
        except:
            logger.error("Auth Modal NOT found - App might be frozen or crashed.")
            driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "no_auth_modal.png"))
            dump_logs(driver, "Auth Modal Missing")

        # Direct Navigation Test (Bypass Auth)
        target_routes = ["/guardian/margin", "/orchestrator"]
        for route in target_routes:
            logger.info(f"Attempting direct navigation to {route}...")
            driver.get(f"{BASE_URL}{route}")
            time.sleep(3)
            dump_logs(driver, f"Direct Nav {route}")
            driver.save_screenshot(os.path.join(SCREENSHOT_DIR, f"direct_{route.replace('/', '_')}.png"))

    except Exception as e:
        logger.error(f"Script Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
