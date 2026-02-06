
import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def check_backend_api():
    base_url = "http://127.0.0.1:5050"
    print(f"Checking Backend API at {base_url}...")
    
    # 1. Health Checks
    try:
        resp = requests.get(f"{base_url}/api/health", timeout=5)
        if resp.status_code == 200:
            print("✅ Backend Health Check Passed")
        else:
            print(f"❌ Backend Health Check Failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Unreachable: {e}")
        return False

    # 2. Check Agents List
    try:
        resp = requests.get(f"{base_url}/api/v1/agents", timeout=5)
        if resp.status_code == 200:
            agents = resp.json()
            count = len(agents)
            print(f"✅ Agents API returned {count} agents")
            if count >= 100:
                 print("✅ Agent Count Verification Passed (Expected > 100)")
            else:
                 print("❌ Agent Count Low - Definitions might be missing")
        else:
             print(f"❌ Agents API Failed or Not Registered: {resp.status_code}")
             return False
    except Exception as e:
        print(f"❌ Agents API Error: {e}")
        return False

    return True

def check_frontend_menu():
    print("\nChecking Frontend Menu with Selenium...")
    frontend_url = "http://127.0.0.1:5173"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for speed
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080") # Ensure desktop view
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(frontend_url)
        wait = WebDriverWait(driver, 10)
        
        # 1. Wait for page load
        print("Waiting for page load...")
        time.sleep(5) # Increased wait
        
        # 2. Click Routes Menu
        # Look for text "Routes" in menu items
        menu_items = driver.find_elements(By.CLASS_NAME, "menu-item")
        routes_menu = None
        
        # DEBUG: Print all found menu items
        print(f"Found {len(menu_items)} menu items:")
        for item in menu_items:
            print(f" - '{item.text}'")
            if "Routes" in item.text:
                routes_menu = item
        
        if routes_menu:
            print("✅ Found 'Routes' menu")
            routes_menu.click()
            
            # Wait for dropdown to be visible
            dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "menu-dropdown")))
            print("✅ 'Routes' dropdown opened")
            
            # Get all dropdown items text
            items = dropdown.find_elements(By.CLASS_NAME, "menu-dropdown-item")
            item_texts = [item.text for item in items]
            
            # Check for quadrant headers
            # Note: The labels in MenuBar.jsx have icons, e.g., "📊 Attack Engine"
            # We look for partial matches
            expected_headers = ["Attack Engine", "Defense Fortress", "Household", "Meta-Cognition", "Scrum of Scrums"]
            
            all_found = True
            print("\nVerifying Menu Items:")
            for header in expected_headers:
                found = any(header in text for text in item_texts)
                if found:
                    print(f"  ✅ Found: {header}")
                else:
                    print(f"  ❌ Missing: {header}")
                    all_found = False
            
            if all_found:
                print("\n✅ All Quadrant Headers Verified")
            else:
                print("\n❌ Some Headers Missing")
                
        else:
            print("❌ 'Routes' menu not found")
            # Capture screenshot
            driver.save_screenshot("frontend_failure.png")
            print("Saved screenshot to frontend_failure.png")
            print("Page Title:", driver.title)
        
    except Exception as e:
        print(f"❌ Frontend Verification Failed: {e}")
        driver.save_screenshot("frontend_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    api_ok = check_backend_api()
    if api_ok:
        check_frontend_menu()
    else:
        print("\nSkipping Frontend check due to Backend failure.")
