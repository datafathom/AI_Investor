"""
Debug script to capture specific console errors on a single route.
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5173"
TEST_ROUTE = "/special/terminal"

def setup_driver() -> webdriver.Chrome:
    """Initialize Chrome driver with console logging enabled."""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def main():
    print(f"🔍 Debugging route: {TEST_ROUTE}")
    driver = setup_driver()
    
    try:
        # Bypass auth
        driver.get(BASE_URL)
        time.sleep(2)
        driver.execute_script("""
            localStorage.setItem('widget_os_bypass', 'true');
            localStorage.setItem('auth_token', 'audit_session_token');
            localStorage.setItem('current_user', JSON.stringify({
                id: 1, username: 'audit_user', email: 'audit@test.com'
            }));
        """)
        driver.refresh()
        time.sleep(3)
        print("✅ Auth bypassed")
        
        # Navigate to test route
        driver.get(f"{BASE_URL}{TEST_ROUTE}")
        time.sleep(7)
        print(f"📄 Page title: {driver.title}")
        
        # Get ALL console logs
        logs = driver.get_log("browser")
        print(f"\n📋 Found {len(logs)} console messages:")
        print("-" * 60)
        
        errors = []
        warnings = []
        for log in logs:
            level = log.get("level", "")
            message = log.get("message", "")
            
            if level in ["SEVERE", "ERROR"]:
                errors.append(message)
                print(f"❌ ERROR: {message[:200]}")
            elif level == "WARNING":
                warnings.append(message)
                print(f"⚠️ WARNING: {message[:200]}")
            else:
                print(f"ℹ️ {level}: {message[:100]}")
        
        print("-" * 60)
        print(f"\n📊 Summary: {len(errors)} errors, {len(warnings)} warnings")
        
        if errors:
            print("\n🔴 ERRORS DETAIL:")
            for i, err in enumerate(errors, 1):
                print(f"\n--- Error {i} ---")
                print(err)
        
        # Keep browser open for manual inspection
        input("\nPress Enter to close browser...")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
