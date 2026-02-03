"""
Final verification script for Strategy page.
Uses headed mode for accurate screenshot.
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def final_verify():
    print("=" * 60)
    print("STRATEGY PAGE FINAL VERIFICATION")
    print("=" * 60)
    
    chrome_options = Options()
    # Use headless with GPU acceleration for better rendering
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Inject bypass before navigation
        print("\n[1] Injecting bypass state via CDP...")
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
                localStorage.setItem('widget_os_bypass', 'true');
                localStorage.setItem('widget_os_token', 'mock-token');
                localStorage.setItem('widget_os_user', JSON.stringify({id: 'verify', username: 'Tester', role: 'admin'}));
            """
        })
        
        print("[2] Navigating to Strategy page...")
        driver.get("http://localhost:5173/analytics/strategy")
        
        print("[3] Waiting 12 seconds for page load and lazy components...")
        time.sleep(12)
        
        # Check for login modal
        print("\n[4] Checking for login modal...")
        modals = driver.find_elements(By.CLASS_NAME, "modal-overlay")
        login_modals = [m for m in modals if m.is_displayed()]
        if login_modals:
            print("  ❌ LOGIN MODAL FOUND - Bypass may not be working")
        else:
            print("  ✅ No login modal visible - Bypass working!")
        
        # Check for page header
        print("\n[5] Checking for page content...")
        headers = driver.find_elements(By.TAG_NAME, "h1")
        found_genomic = False
        for h in headers:
            if h.is_displayed() and "Genomic" in h.text:
                print(f"  ✅ Found header: {h.text}")
                found_genomic = True
        if not found_genomic:
            print("  ⚠️ 'Genomic Evolution Lab' header not found")
        
        # Check for error boundaries
        print("\n[6] Checking for widget errors...")
        page_source = driver.page_source
        if "Widget Error" in page_source:
            print("  ⚠️ Widget errors present on page")
            error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Widget Error')]")
            for el in error_elements[:5]:
                print(f"    - {el.text[:100]}")
        else:
            print("  ✅ No widget errors found!")
        
        # Check for fatal error boundary
        if "Something went wrong" in page_source:
            print("  ❌ FATAL: Page-level error boundary triggered!")
        else:
            print("  ✅ No fatal error boundary!")
        
        # Check console logs for SEVERE errors
        print("\n[7] Checking browser console for SEVERE errors...")
        logs = driver.get_log('browser')
        severe_count = 0
        for entry in logs:
            if entry['level'] == 'SEVERE':
                severe_count += 1
                if severe_count <= 3:
                    print(f"  [{entry['level']}] {entry['message'][:150]}...")
        if severe_count > 3:
            print(f"  ... and {severe_count - 3} more SEVERE errors")
        if severe_count == 0:
            print("  ✅ No SEVERE console errors!")
        
        # Save screenshot
        screenshot_path = os.path.abspath("strategy_final_verify.png")
        driver.save_screenshot(screenshot_path)
        print(f"\n[8] Screenshot saved: {screenshot_path}")
        
        # Final verdict
        print("\n" + "=" * 60)
        if not login_modals and "Something went wrong" not in page_source:
            print("✅ VERIFICATION PASSED: Strategy page is accessible!")
        else:
            print("❌ VERIFICATION FAILED: Issues detected")
        print("=" * 60)

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    final_verify()
