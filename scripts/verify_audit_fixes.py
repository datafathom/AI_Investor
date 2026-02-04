import json
import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Hardcoded path for this task
AUDIT_FILE = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\notes\FrontEndAudit_2_3_26\AuditResults_1770168107.json"
BASE_URL = "http://localhost:5173"

def setup_driver():
    options = Options()
    options.add_argument("--headless") # Comment out to see the browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def verify_fixes():
    print(f"Loading audit results from: {AUDIT_FILE}")
    with open(AUDIT_FILE, 'r') as f:
        data = json.load(f)
    
    driver = setup_driver()
    results = data
    
    updated_count = 0
    
    try:
        # First ensure we can login or hit the dashboard
        print("Navigating to Dashboard root...")
        driver.get(BASE_URL)
        time.sleep(5) # Wait for initial load
        
        for item in results:
            if item.get("status") == "Failed":
                route = item.get("route")
                print(f"\nVerifying route: {route}")
                
                start_time = time.time()
                driver.get(f"{BASE_URL}{route}")
                time.sleep(3) # Wait for page load
                
                # Check logs
                logs = driver.get_log('browser')
                errors = [log for log in logs if log['level'] == 'SEVERE']
                
                load_time = (time.time() - start_time) * 1000
                
                if not errors:
                    print(f"✅ Success! No console errors.")
                    item["status"] = "Success"
                    item["fail_reason"] = None
                    item["page_load_time"] = round(load_time, 2)
                    updated_count += 1
                else:
                    print(f"❌ Still Failing. Found {len(errors)} errors.")
                    for e in errors:
                        print(f"  - {e['message']}")
                    # Update fail reason if it changed? For now keep it or update it.
                    item["fail_reason"] = f"Console Errors: {errors[0]['message']}"
                    
                # Save progress periodically
                if updated_count % 5 == 0:
                     with open(AUDIT_FILE, 'w') as f:
                        json.dump(data, f, indent=2)
                        
    except Exception as e:
        print(f"Script error: {e}")
    finally:
        driver.quit()
        
        # Final save
        with open(AUDIT_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
    print(f"\nVerification complete. Updated {updated_count} routes to Success.")

if __name__ == "__main__":
    verify_fixes()
