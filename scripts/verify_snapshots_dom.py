import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def verify_snapshots_final():
    print("🚀 Verifying Snapshots (Final Attempt)...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("http://localhost:5173")
        time.sleep(8)
        
        # 1. Restore a window using JS click
        icons = driver.find_elements(By.CLASS_NAME, "taskbar-icon")
        if icons:
            print(f"🖱️ Clicking Icon 0 to restore window...")
            driver.execute_script("arguments[0].click();", icons[0])
            time.sleep(3) # Wait for window to open and snapshot to trigger
            
            # Hover to check for snapshot-img
            print("🔍 Checking for snapshot image in hover preview...")
            actions = ActionChains(driver)
            actions.move_to_element(icons[0]).perform()
            time.sleep(1.5)
            
            try:
                snapshot = driver.find_element(By.CLASS_NAME, "snapshot-img")
                print("✅ Found snapshot-img in preview!")
                driver.save_screenshot("snapshot_final_success.png")
            except:
                print("❌ Snapshot-img NOT found in preview.")
                # Let's try to minimize and check again
                print("📉 Attempting to minimize to trigger snapshot...")
                minimize_btns = driver.find_elements(By.CLASS_NAME, "btn-minimize")
                if minimize_btns:
                    driver.execute_script("arguments[0].click();", minimize_btns[0])
                    time.sleep(2)
                    actions.move_to_element(icons[0]).perform()
                    time.sleep(1)
                    try:
                        snapshot = driver.find_element(By.CLASS_NAME, "snapshot-img")
                        print("✅ Found snapshot-img in preview after minimize!")
                        driver.save_screenshot("snapshot_final_success_minimize.png")
                    except:
                        print("❌ Still no snapshot-img.")
                        driver.save_screenshot("snapshot_final_fail.png")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_snapshots_final()
