from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def verify_deployment():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Path to snapshots
    os.makedirs("screenshots", exist_ok=True)
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("1. Opening http://localhost:5173...")
        driver.get("http://localhost:5173")
        
        # Wait for page load
        time.sleep(5)
        
        # Capture Title
        print(f"Page Title: {driver.title}")
        
        # Capture Console Errors
        logs = driver.get_log("browser")
        errors = [entry for entry in logs if entry['level'] == 'SEVERE']
        
        if errors:
            print(f"❌ CONSOLE ERRORS FOUND ({len(errors)}):")
            for error in errors:
                print(f"  - {error['message']}")
        else:
            print("✅ No Console Errors Detected.")
            
        # check for specific elements
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
            print("✅ UI Elements detected.")
        except:
            print("❌ UI Elements NOT detected (Blank screen?).")

        # Take Screenshot
        driver.save_screenshot("screenshots/verification_step_1.png")
        print("📸 Screenshot saved to screenshots/verification_step_1.png")
        
        # Try navigating to /orbital
        print("2. Navigating to /orbital...")
        driver.get("http://localhost:5173/orbital")
        time.sleep(3)
        driver.save_screenshot("screenshots/verification_step_2_orbital.png")
        print("📸 Screenshot saved to screenshots/verification_step_2_orbital.png")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_deployment()
