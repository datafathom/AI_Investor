"""
===============================================================================
FILE: scripts/verify_all_routes.py
ROLE: Comprehensive Route & Widget Verification Script (Auth-First, Debug-Heavy)
PURPOSE: Performs a full E2E walkthrough with robust error handling:
         1. Create test account via API
         2. Verify account via API
         3. Login via Selenium UI
         4. Verify all routes one by one with 3s render delay
===============================================================================
"""

import os
import sys
import time
import re
import logging
import json
import urllib.request
import traceback
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Setup path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
FRONTEND_URL = "http://127.0.0.1:5173"
BACKEND_URL = "http://127.0.0.1:5050"
ROUTES_FILE = PROJECT_ROOT / "docs" / "_PLANS" / "Services_Mapped_To_Frontend_Pages" / "_NEW_ROUTES.txt"
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "_PLANS" / "Services_Mapped_To_Frontend_Pages" / "Success_Screen_Shot"
PAGE_LOAD_TIMEOUT = 20  # seconds

# Test Credentials
TEST_EMAIL = f"test_{int(time.time())}@aiinvestor.com"
TEST_PASSWORD = "Password123!"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / "scripts" / "verification.log", mode="w", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


def api_request(path: str, method: str = "GET", data: Dict = None) -> Dict:
    """Helper to make backend API requests."""
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
        logger.error(f"API request to {path} failed: {e}")
        return {"success": False, "detail": str(e)}


def parse_routes_from_file(file_path: Path) -> List[Dict[str, str]]:
    """Parse routes from _NEW_ROUTES.txt file."""
    routes = []
    seen = set()
    
    if not file_path.exists():
        logger.error(f"Routes file not found: {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('[!'):
                continue
            
            # Extract URL from line
            match = re.search(r'http://localhost:5173(/[^\s]*)', line)
            if match:
                route = match.group(1)
                if route not in seen:
                    seen.add(route)
                    phase_match = re.search(r'Phase[_\s]*(\d+)', line)
                    phase = phase_match.group(1) if phase_match else "?"
                    routes.append({"route": route, "phase": phase})
    
    return routes


def check_console_errors(driver: webdriver.Chrome) -> List[str]:
    """Capture console errors."""
    errors = []
    try:
        for entry in driver.get_log('browser'):
            if entry['level'] in ('SEVERE', 'ERROR'):
                msg = entry['message']
                if 'favicon.ico' in msg or 'socket.io' in msg:
                    continue
                errors.append(msg)
    except:
        pass
    return errors


def run_verification():
    # 1. Start setup
    logger.info(f"🚀 Starting verification with account: {TEST_EMAIL}")
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Register User via API
    logger.info("Step 1: Registering test user via API...")
    reg_resp = api_request("/auth/register", method="POST", data={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    if not reg_resp.get("success"):
        logger.error(f"Registration failed: {reg_resp}")
        return

    # 3. Verify User via API
    logger.info("Step 2: Verifying account via API...")
    ver_resp = api_request(f"/auth/verify/{TEST_EMAIL}", method="GET")
    if not ver_resp.get("success"):
        logger.error(f"Verification failed: {ver_resp}")
        return

    # 4. Initialize Selenium
    logger.info("Initializing Selenium WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless") # Uncomment if you want headless
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        return

    try:
        # 5. Browser Login
        logger.info("Step 3: Navigating to Frontend for Login...")
        driver.get(FRONTEND_URL)
        time.sleep(5) # Wait for initial JS execution

        logger.info("Attempting to find Login Modal...")
        try:
            # Wait for any input to appear (Login Modal)
            # We use presence_of_element_located to be safe
            email_field = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            logger.info("Found email field. Filling credentials...")
            
            pass_field = driver.find_element(By.NAME, "password")
            
            email_field.send_keys(TEST_EMAIL)
            pass_field.send_keys(TEST_PASSWORD)
            
            # Click Login Button
            # We look for the button with class "auth-button"
            submit_btn = driver.find_element(By.CLASS_NAME, "auth-button")
            logger.info("Clicking sign-in button...")
            submit_btn.click()
            
            # Wait for modal to disappear
            logger.info("Waiting for auth-modal to disappear...")
            WebDriverWait(driver, 15).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "auth-modal"))
            )
            logger.info("✅ Login successful, modal dismissed.")
            
        except TimeoutException:
            logger.error("❌ TIMEOUT: Login modal/inputs not found or didn't close.")
            driver.save_screenshot(str(SCREENSHOT_DIR / "login_timeout_diag.png"))
            with open(PROJECT_ROOT / "scripts" / "diagnostics_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            return
        except Exception as e:
            logger.error(f"❌ ERROR during login: {e}")
            logger.error(traceback.format_exc())
            driver.save_screenshot(str(SCREENSHOT_DIR / "login_error_diag.png"))
            return

        # 6. Verify Routes
        routes = parse_routes_from_file(ROUTES_FILE)
        logger.info(f"Step 4: Verifying {len(routes)} routes one by one...")
        
        results = {"passed": 0, "failed": 0, "skipped": 0}
        
        for i, r in enumerate(routes, 1):
            route = r["route"]
            phase = r["phase"]
            logger.info(f"[{i}/{len(routes)}] Testing Phase {phase}: {route}")
            
            try:
                driver.get(f"{FRONTEND_URL}{route}")
                time.sleep(3) # Wait 3 full seconds as requested by user
                
                # Checks
                errors = check_console_errors(driver)
                
                # Check for "Login" or "Welcome Back" which implies session lost
                page_text = driver.find_element(By.TAG_NAME, "body").text
                if "Welcome Back" in page_text or "Create Account" in page_text:
                    logger.error(f"    ❌ FAILED: Redirected to login page at {route}")
                    driver.save_screenshot(str(SCREENSHOT_DIR / f"fail_auth_{phase}_{route.replace('/', '_')}.png"))
                    results["failed"] += 1
                    continue

                if errors:
                    logger.warning(f"    ⚠️ Console errors detected: {len(errors)}")
                    for err in errors[:3]: # Log first 3
                        logger.warning(f"        {err}")
                
                # Rendering check
                content_len = len(page_text.strip())
                
                # STRICTOR VALIDATION: Search for known failure strings
                error_keywords = [
                    "WORKSTATION_NOT_FOUND", 
                    "ERROR: PAGE_NOT_FOUND", 
                    "404 - NOT FOUND",
                    "UNDER_CONSTRUCTION",
                    "ROUTE_ERROR"
                ]
                
                found_errors = [kw for kw in error_keywords if kw in page_text.upper()]
                
                if content_len < 100: # Increased threshold
                    logger.error(f"    ❌ FAILED: Page seems too empty (length {content_len})")
                    driver.save_screenshot(str(SCREENSHOT_DIR / f"fail_empty_{phase}_{route.replace('/', '_')}.png"))
                    results["failed"] += 1
                elif found_errors:
                    logger.error(f"    ❌ FAILED: UI Error detected: {found_errors} at {route}")
                    driver.save_screenshot(str(SCREENSHOT_DIR / f"fail_ui_err_{phase}_{route.replace('/', '_')}.png"))
                    results["failed"] += 1
                elif "Welcome Back" in page_text or "Create Account" in page_text or "Login" in page_text and content_len < 1000:
                    # Double check if redirected to login despite being logged in
                    logger.error(f"    ❌ FAILED: Potentially redirected to login at {route}")
                    driver.save_screenshot(str(SCREENSHOT_DIR / f"fail_auth_redirect_{phase}_{route.replace('/', '_')}.png"))
                    results["failed"] += 1
                else:
                    logger.info("    ✅ PASS")
                    results["passed"] += 1
            except Exception as e:
                logger.error(f"    ❌ ERROR testing route {route}: {e}")
                results["failed"] += 1

        # 7. Final Report
        logger.info("============================================================")
        logger.info("VERIFICATION SUMMARY")
        logger.info(f"Total Routes: {len(routes)}")
        logger.info(f"Passed:       {results['passed']}")
        logger.info(f"Failed:       {results['failed']}")
        logger.info("============================================================")

        if results["failed"] == 0:
            logger.info("🎉 ALL ROUTES VERIFIED SUCCESSFULLY!")
            driver.get(FRONTEND_URL)
            time.sleep(3)
            driver.save_screenshot(str(SCREENSHOT_DIR / "final_success.png"))
        else:
            logger.info(f"⚠️ Verification completed with {results['failed']} failures.")

    except Exception as e:
        logger.critical(f"UNEXPECTED CRITICAL FAILURE: {e}")
        logger.critical(traceback.format_exc())
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_verification()
