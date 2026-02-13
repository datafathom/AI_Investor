import os
import time
import json
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")
logger = logging.getLogger(__name__)

FRONTEND_URL = "http://127.0.0.1:5173"
BACKEND_URL = "http://127.0.0.1:5050"
AUDIT_DIR = Path("scripts/audits")
AUDIT_DIR.mkdir(exist_ok=True)

def audit_route(path):
    target_url = f"{FRONTEND_URL}{path}"
    logger.info(f"🚀 Auditing route: {target_url}")
    
    # 1. Login via API to get token
    logger.info("Logging in via API...")
    user_email = "test_audit@aiinvestor.com"
    user_pass = "AuditPass123!"
    
    # Register/Login
    requests.post(f"{BACKEND_URL}/api/v1/auth/register", json={
        "email": user_email, "full_name": "Audit User", "password": user_pass
    })
    requests.post(f"{BACKEND_URL}/api/v1/auth/verify", json={"email": user_email})
    resp = requests.post(f"{BACKEND_URL}/api/v1/auth/login", json={"email": user_email, "password": user_pass})
    
    if resp.status_code != 200:
        logger.error(f"Login failed: {resp.text}")
        return
    
    token = resp.json().get("access_token")
    logger.info("Login successful.")

    # 2. Setup Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enable console log capture
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate and set token in localStorage
        driver.get(FRONTEND_URL)
        driver.execute_script(f"localStorage.setItem('token', '{token}');")
        driver.execute_script(f"localStorage.setItem('user', JSON.stringify({{ 'email': '{user_email}' }}));")
        
        # Go to target route
        driver.get(target_url)
        logger.info(f"Navigated to {target_url}")
        
        # Wait for page load
        time.sleep(5)
        
        # Capture Screenshot
        safe_name = path.replace("/", "_").strip("_") or "root"
        screenshot_path = AUDIT_DIR / f"{safe_name}.png"
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"📸 Screenshot saved to {screenshot_path}")
        
        # Capture Console Logs
        logs = driver.get_log("browser")
        log_path = AUDIT_DIR / f"{safe_name}_console.json"
        with open(log_path, "w") as f:
            json.dump(logs, f, indent=2)
        logger.info(f"📜 Console logs saved to {log_path}")
        
        # Summarize Errors
        errors = [l for l in logs if l["level"] == "SEVERE"]
        if errors:
            logger.warning(f"❌ Found {len(errors)} SEVERE errors on {path}:")
            for e in errors:
                logger.warning(f"   - {e['message']}")
        else:
            logger.info(f"✅ No SEVERE errors found on {path}.")

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit_route.py /path/to/route")
        sys.exit(1)
    audit_route(sys.argv[1])
