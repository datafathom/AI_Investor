
import os
import time
import json
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:5050"
TIMESTAMP = datetime.now().strftime("%Y_%M_%D_%H%M%S").replace("/", "")
EMAIL = f"audit_2026_01_27_{TIMESTAMP}@fathom.ai" # Follow the @fathom.ai protocol
PASSWORD = "MockPassword123!"
SCREENSHOT_DIR = "frontend2/screenshots/audit_2026_01_27"
WAIT_TIME_STABLE = 7  # Seconds per page according to Audit_FrontEndPlan.md

# Routes to audit
ROUTES = [
    "/workspace/terminal",
    "/workspace/mission-control",
    "/analytics/political",
    "/analytics/strategy",
    "/workspace/debate",
    "/workspace/autocoder",
    "/workspace/vr",
    "/analytics/options",
    "/portfolio/backtest",
    "/strategist/estate",
    "/strategist/impact",
    "/strategist/corporate",
    "/architect/system",
    "/architect/api",
    "/guardian/compliance/audit",
    "/guardian/scenarios",
    "/guardian/margin",
    "/mobile",
    "/portfolio/brokerage",
    "/workspace/auto-coder",
    "/portfolio/attribution",
    "/portfolio/fixed-income",
    "/portfolio/crypto",
    "/portfolio/tax",
    "/observer/macro",
    "/guardian/compliance",
    "/strategist/currency",
    "/scanner/global",
    "/assets",
    "/portfolio/cash-flow",
    "/zen",
    "/tenant",
    "/portfolio/advanced-analytics",
    "/portfolio/optimization",
    "/portfolio/risk",
    "/portfolio/tax-optimization",
    "/planning/financial",
    "/planning/retirement",
    "/budgeting",
    "/trading/options",
    "/trading/paper",
    "/trading/algorithmic",
    "/planning/estate",
    "/billing/payments",
    "/credit/monitoring",
    "/research/reports",
    "/social/trading",
    "/community/forums",
    "/education",
    "/charting/advanced",
    "/trading/advanced-orders",
    "/enterprise",
    "/institutional",
    "/ml/training",
    "/integrations",
    "/developer/platform",
    "/marketplace",
    "/news/sentiment",
    "/watchlists/alerts",
    "/ai/predictions",
    "/ai/assistant",
    "/legal/terms",
    "/legal/privacy"
]

def setup_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless") # Useful for server runs
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def register_via_ui(driver):
    logger.info(f"Navigating to Homepage")
    driver.get(BASE_URL)
    time.sleep(15) # Give it time to show the modal
    
    try:
        # Check if Modal is already    try:
        logger.info("Detecting Login Modal")
        # Wait up to 15s for auth modal
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "auth-modal")))
        logger.info("Auth modal detected")#ch to Registration
        logger.info("Switching to Registration mode")
        toggle_reg = driver.find_element(By.CLASS_NAME, "switch-auth")
        toggle_reg.click()
        time.sleep(1)
        
        # 2. Fill Registration Form
        logger.info(f"Filling Registration for: {EMAIL}")
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
        
        email_input.send_keys(EMAIL)
        pass_input.send_keys(PASSWORD)
        
        # 3. Submit
        driver.find_element(By.CLASS_NAME, "auth-button").click()
        logger.info("Registration submitted")
        time.sleep(3)
        
    except Exception as e:
        logger.error(f"Registration UI flow failed: {e}")
        driver.save_screenshot(f"{SCREENSHOT_DIR}/fail/registration_ui_failure.png")
        raise

def verify_email_api():
    logger.info(f"Bypassing Email Verification per Protocol for {EMAIL}")
    try:
        resp = requests.get(f"{API_URL}/api/auth/verify-email?email={EMAIL}&token=mock_verify_token")
        logger.info(f"Verification status: {resp.status_code}")
    except Exception as e:
        logger.error(f"Verification request failed: {e}")

def login_ui(driver):
    logger.info("Ensuring Authenticated State")
    driver.get(BASE_URL)
    time.sleep(5)
    
    # Check if already logged in (look for 'Account' menu text or profile name)
    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "Logout" in body_text or "Signed in as" in body_text:
            logger.info("Already logged in. Skipping UI login flow.")
            return
    except:
        pass

    logger.info("Not logged in. Proceeding with UI login.")
    
    try:
        # If modal is not there, open it via Account (fallback)
        if len(driver.find_elements(By.CLASS_NAME, "auth-modal")) == 0:
            logger.info("Modal not found, attempting MenuBar Account -> Sign In")
            account_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-item') and contains(text(), 'Account')]")))
            account_menu.click()
            signin_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-dropdown-item') and contains(text(), 'Sign In')]")))
            signin_btn.click()
        
        # Ensure we are in Login mode
        modal_header = driver.find_element(By.XPATH, "//div[contains(@class, 'modal-header')]//h2").text
        if "Create Account" in modal_header:
            logger.info("Switching to Login mode")
            driver.find_element(By.CLASS_NAME, "switch-auth").click()
            time.sleep(1)

        # Fill Login
        email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
        
        email_input.send_keys(EMAIL)
        pass_input.send_keys(PASSWORD)
        
        driver.find_element(By.CLASS_NAME, "auth-button").click()
        
        # Wait for Landing
        WebDriverWait(driver, 20).until(EC.url_contains("/workspace"))
        logger.info("Login Successful")
    except Exception as e:
        logger.error(f"Login UI flow failed: {e}")
        driver.save_screenshot(f"{SCREENSHOT_DIR}/fail/login_ui_failure.png")
        raise
    
    # Skip Onboarding via UI if visible
    time.sleep(3)
    skip_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Finish')]")
    if skip_btns:
        skip_btns[0].click()
        logger.info("Onboarding Skipped via UI")

def check_overlap(driver):
    """
    Mathematical Overlap Detection (AABB)
    """
    script = """
    const containers = Array.from(document.querySelectorAll('.widget-container, .glass-panel, .rounded-xl'));
    const rects = containers.map(el => {
        const r = el.getBoundingClientRect();
        return { id: el.id || el.className, left: r.left, right: r.right, top: r.top, bottom: r.bottom };
    });
    
    const overlaps = [];
    for (let i = 0; i < rects.length; i++) {
        for (let j = i + 1; j < rects.length; j++) {
            const r1 = rects[i];
            const r2 = rects[j];
            if (r1.left < r2.right && r1.right > r2.left && r1.top < r2.bottom && r1.bottom > r2.top) {
                overlaps.push({ a: r1.id, b: r2.id });
            }
        }
    }
    return overlaps;
    """
    overlaps = driver.execute_script(script)
    return overlaps

def audit_page(driver, route):
    safe_name = route.replace("/", "_").strip("_") or "home"
    logger.info(f"AUDITING: {route}")
    
    driver.get(f"{BASE_URL}{route}")
    
    # Use WebDriverWait instead of harder sleep
    try:
        WebDriverWait(driver, WAIT_TIME_STABLE).until(EC.presence_of_element_located((By.CLASS_NAME, "institutional-os-container")))
    except:
        logger.warning(f"Timeout waiting for app-container on {route}")

    # AGGRESSIVE ONBOARDING BYPASS
    skip_selectors = [
        "//button[contains(text(), 'Skip')]",
        "//button[contains(text(), 'Finish')]",
        "//button[contains(@class, 'skip')]",
        "//div[contains(@class, 'onboarding')]//button"
    ]
    for selector in skip_selectors:
        btns = driver.find_elements(By.XPATH, selector)
        if btns:
            try:
                btns[0].click()
                logger.info(f"Bypassed onboarding on {route}")
                time.sleep(1) # Small fade time
            except:
                pass
    
    # Detection Markers
    body_text = driver.find_element(By.TAG_NAME, "body").text
    is_fail = any(err in body_text for err in ["404", "Not Found", "Application Error", "React Crash"])
    
    # Gold Standard Checks
    has_os_bleed = len(driver.find_elements(By.CLASS_NAME, "os-bleed")) > 0
    has_glass_header = len(driver.find_elements(By.CLASS_NAME, "glass-panel-header")) > 0
    
    # AABB Overlap Detection
    overlaps = check_overlap(driver)
    if overlaps:
        logger.error(f"OVERLAP DETECTED on {route}: {overlaps}")
        is_fail = True
    
    if not has_os_bleed:
        logger.warning(f"MISSING .os-bleed on {route}")
        
    suffix = "fail" if is_fail else "success"
    
    # Robust Screenshots
    driver.save_screenshot(f"{SCREENSHOT_DIR}/{suffix}/{safe_name}.png")
    
    # Capture Scrolled View
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.save_screenshot(f"{SCREENSHOT_DIR}/{suffix}/{safe_name}_scrolled.png")
    
    # Log Results
    res = {
        "route": route,
        "status": suffix,
        "os_bleed": has_os_bleed,
        "glass_panel": has_glass_header,
        "overlaps": overlaps
    }
    return res

def main():
    if not os.path.exists(f"{SCREENSHOT_DIR}/success"): os.makedirs(f"{SCREENSHOT_DIR}/success")
    if not os.path.exists(f"{SCREENSHOT_DIR}/fail"): os.makedirs(f"{SCREENSHOT_DIR}/fail")
    
    driver = setup_driver()
    results = []
    try:
        register_via_ui(driver)
        verify_email_api()
        login_ui(driver)
        
        for route in ROUTES:
            try:
                res = audit_page(driver, route)
                results.append(res)
            except Exception as e:
                logger.error(f"Audit failed for {route}: {e}")
                
        with open(f"{SCREENSHOT_DIR}/audit_results.json", "w") as f:
            json.dump(results, f, indent=2)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
