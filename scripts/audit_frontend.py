"""
Frontend Route Audit Script
Audits all frontend routes using Selenium with console error detection.
Saves screenshots to Success/Failed folders based on results.
"""
import os
import sys
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
BASE_URL = "http://127.0.0.1:5173"
OUTPUT_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\notes\FrontEndAudit_2_6_26"
SUCCESS_DIR = os.path.join(OUTPUT_DIR, "Success")
FAILED_DIR = os.path.join(OUTPUT_DIR, "Failed")
MAX_RETRIES = 4
WAIT_TIME = 5  # seconds to wait for page load

# All routes to audit
ROUTES = [
    # Special Operations
    "/special/terminal",
    "/special/mission-control",
    "/special/missions",
    "/special/scrum",
    "/special/fleet",
    "/special/mobile",
    "/special/vr",
    "/special/zen",
    "/special/political",
    "/special/strategy",
    "/special/debate",
    "/special/paper",
    
    # Department Dashboards
    "/dept/orchestrator",
    "/dept/architect",
    "/dept/data-scientist",
    "/dept/strategist",
    "/dept/trader",
    "/dept/physicist",
    "/dept/hunter",
    "/dept/sentry",
    "/dept/steward",
    "/dept/guardian",
    "/dept/lawyer",
    "/dept/auditor",
    "/dept/envoy",
    "/dept/front-office",
    "/dept/historian",
    "/dept/stress-tester",
    "/dept/refiner",
    "/dept/banker",
    
    # Account & Settings
    "/account",
    "/settings",
    
    # Sub-module routes (sample)
    "/orchestrator/graph",
    "/architect/health",
    "/architect/api",
    "/trader/scanner",
    "/trader/options",
    "/strategist/brokerage",
    "/strategist/backtest",
    "/data-scientist/autocoder",
    "/data-scientist/sandbox",
    "/data-scientist/debate",
    "/hunter/news",
    "/hunter/social",
    "/legal/compliance",
    "/legal/audit",
    "/guardian/risk",
    "/guardian/credit",
]


def setup_driver() -> webdriver.Chrome:
    """Initialize Chrome driver with console logging enabled."""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Enable console log capture
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def bypass_auth(driver: webdriver.Chrome) -> None:
    """Set localStorage to bypass authentication."""
    driver.get(BASE_URL)
    time.sleep(2)
    
    driver.execute_script("""
        localStorage.setItem('widget_os_bypass', 'true');
        localStorage.setItem('auth_token', 'audit_session_token');
        localStorage.setItem('current_user', JSON.stringify({
            id: 1, 
            username: 'audit_user', 
            email: 'audit@test.com'
        }));
    """)
    driver.refresh()
    time.sleep(3)
    print("✅ Auth bypassed successfully")


def get_console_errors(driver: webdriver.Chrome) -> list[str]:
    """Get console errors from browser logs, filtering non-blocking issues."""
    # Patterns to IGNORE (non-blocking background API errors)
    IGNORE_PATTERNS = [
        "Failed to load resource",  # Background API 500s
        "net::ERR_",  # Network errors from optional APIs
        "favicon.ico",  # Favicon 404
        "socket.io",  # Socket connection attempts
        "WebSocket",  # WebSocket connection attempts
        "/api/v1/presence",  # Presence service calls
        "/api/v1/metrics",  # Metrics endpoints
        "/api/v1/health",  # Health check calls
        "/api/v1/onboarding",  # Onboarding status calls
        "ResizeObserver loop",  # Benign React warning
    ]
    
    errors = []
    try:
        logs = driver.get_log("browser")
        for log in logs:
            if log["level"] in ["SEVERE", "ERROR"]:
                message = log["message"]
                # Check if this is a blocking error or just noise
                is_noise = any(pattern.lower() in message.lower() for pattern in IGNORE_PATTERNS)
                if not is_noise:
                    errors.append(message)
    except Exception as e:
        print(f"  ⚠️ Could not get console logs: {e}")
    return errors



def sanitize_filename(route: str) -> str:
    """Convert route to valid filename."""
    return route.replace("/", "_").strip("_") or "home"


def audit_route(driver: webdriver.Chrome, route: str, attempt: int = 1) -> dict:
    """Audit a single route."""
    result = {
        "route": route,
        "status": "failed",
        "console_errors": [],
        "attempts": attempt,
        "notes": ""
    }
    
    try:
        full_url = f"{BASE_URL}{route}"
        print(f"  Navigating to {full_url}...")
        driver.get(full_url)
        time.sleep(WAIT_TIME)
        
        # Check for 404 or error pages
        page_source = driver.page_source.lower()
        if "404" in page_source or "not found" in page_source:
            result["notes"] = "Page shows 404 or Not Found"
            return result
        
        # Get console errors
        errors = get_console_errors(driver)
        result["console_errors"] = errors
        
        if errors:
            result["notes"] = f"Found {len(errors)} console error(s)"
            return result
        
        # Success
        result["status"] = "success"
        result["notes"] = "Page loaded without errors"
        
    except Exception as e:
        result["notes"] = f"Exception: {str(e)}"
    
    return result


def save_screenshot(driver: webdriver.Chrome, route: str, success: bool) -> str:
    """Save screenshot to appropriate folder."""
    folder = SUCCESS_DIR if success else FAILED_DIR
    filename = f"{sanitize_filename(route)}.png"
    filepath = os.path.join(folder, filename)
    driver.save_screenshot(filepath)
    return filepath


def run_audit() -> None:
    """Run the full frontend audit."""
    print("=" * 60)
    print("🔍 Frontend Route Audit Starting")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print("=" * 60)
    
    # Ensure directories exist
    os.makedirs(SUCCESS_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)
    
    driver = setup_driver()
    results = []
    
    try:
        bypass_auth(driver)
        
        for i, route in enumerate(ROUTES, 1):
            print(f"\n[{i}/{len(ROUTES)}] Auditing: {route}")
            
            result = None
            for attempt in range(1, MAX_RETRIES + 1):
                print(f"  Attempt {attempt}/{MAX_RETRIES}...")
                result = audit_route(driver, route, attempt)
                
                if result["status"] == "success":
                    break
                elif attempt < MAX_RETRIES:
                    print(f"  ⚠️ Failed, retrying...")
                    time.sleep(2)
            
            # Save screenshot
            screenshot_path = save_screenshot(driver, route, result["status"] == "success")
            result["screenshot"] = screenshot_path
            
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"  {status_icon} {result['status'].upper()} - {result['notes']}")
            print(f"  📸 Screenshot: {screenshot_path}")
            
            results.append(result)
        
    finally:
        driver.quit()
    
    # Generate summary report
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count
    
    print("\n" + "=" * 60)
    print("📊 AUDIT SUMMARY")
    print("=" * 60)
    print(f"Total Routes: {len(results)}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"Success Rate: {(success_count/len(results)*100):.1f}%")
    
    # Save JSON report
    report_path = os.path.join(OUTPUT_DIR, "audit_results.json")
    with open(report_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_routes": len(results),
            "success_count": success_count,
            "failed_count": failed_count,
            "success_rate": f"{(success_count/len(results)*100):.1f}%",
            "results": results
        }, f, indent=2)
    print(f"\n📄 Report saved: {report_path}")
    
    # List failed routes
    if failed_count > 0:
        print("\n❌ FAILED ROUTES:")
        for r in results:
            if r["status"] == "failed":
                print(f"  - {r['route']}: {r['notes']}")


if __name__ == "__main__":
    run_audit()
