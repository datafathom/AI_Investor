
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DebugLogin")

def test_login():
    options = Options()
    # options.add_argument("--headless") # Comment out to see browser if running locally (but we can't)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    logger.info("Initializing Driver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "http://localhost:5173"
        logger.info(f"Navigating to {url}...")
        driver.get(url)
        
        logger.info("Waiting for page load...")
        time.sleep(5)
        
        logger.info("Checking for Login Modal or Dashboard...")
        # Check for specific elements
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "root"))
            )
            logger.info("Root element found.")
        except:
            logger.error("Root element NOT found.")
            
        screenshot_path = "debug_login_state.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved to {screenshot_path}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        driver.quit()
        logger.info("Driver quit.")

if __name__ == "__main__":
    test_login()
