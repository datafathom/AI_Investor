import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_workflows():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    print("Installing/Updating ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        base_url = "http://localhost:5173"
        print(f"Opening URL: {base_url}")
        driver.get(base_url)
        
        wait = WebDriverWait(driver, 15)
        
        # Login (if modal appears)
        print("Checking for Login Modal...")
        try:
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_input = driver.find_element(By.NAME, "password")
            print("Found login fields, performing login...")
            email_input.send_keys("admin")
            password_input.send_keys("makeMoney")
            driver.find_element(By.CLASS_NAME, "auth-button").click()
            time.sleep(3)
        except Exception:
            print("Login modal not detected or already logged in.")
        
        departments_to_check = [
            {"id": "orchestrator", "name": "The Orchestrator", "workflows": ["COMMAND INTERPRETER", "EMERGENCY KILL-SWITCH"]},
            {"id": "trader", "name": "The Trader", "workflows": ["SNIPER", "EXIT MANAGER", "POSITION SIZER"]},
            {"id": "physicist", "name": "The Physicist", "workflows": ["THETA COLLECTOR", "DELTA HEDGER"]}
        ]
        
        screenshot_dir = "screenshots/verify_workflows"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            
        for dept in departments_to_check:
            url = f"{base_url}/dept/{dept['id']}"
            print(f"\nNavigating to {dept['name']} ({url})...")
            driver.get(url)
            time.sleep(5) # Wait for viz and metrics to load
            
            screenshot_path = f"{screenshot_dir}/{dept['id']}_workflow_check.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            print(f"Verifying workflow buttons for {dept['name']}...")
            
            # Debug: Check if metric-panel exists
            try:
                panel = driver.find_element(By.CLASS_NAME, "metric-panel")
                print(" [V] Found .metric-panel")
                buttons = panel.find_elements(By.CLASS_NAME, "workflow-btn")
                print(f" [V] Found {len(buttons)} workflow buttons in panel")
                for i, b in enumerate(buttons):
                    print(f"     Button {i}: '{b.text}'")
            except Exception:
                print(" [X] .metric-panel NOT FOUND")
                # Print a bit of page source for debugging
                body_text = driver.find_element(By.TAG_NAME, "body").text[:500]
                print(f"     Body beginning: {body_text}")

            for wf_label in dept['workflows']:
                try:
                    # Find button by text content (case insensitive-ish with upper in label)
                    xpath = f"//button[contains(@class, 'workflow-btn') and contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), '{wf_label}')]"
                    btn = driver.find_element(By.XPATH, xpath)
                    print(f" [V] Found workflow button: {wf_label}")
                except Exception:
                    print(f" [X] MISSING workflow button: {wf_label}")

        print("\nVerification Complete.")
                    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        driver.save_screenshot("screenshots/verify_workflows/critical_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_workflows()
