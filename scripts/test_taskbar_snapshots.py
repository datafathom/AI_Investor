import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def verify_taskbar_snapshots():
    print("🚀 Starting Taskbar Snapshot Verification...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("http://localhost:5173")
        time.sleep(5) # Wait for initial render and windows to open
        
        # 1. Take a screenshot of the initial state
        driver.save_screenshot("initial_state.png")
        print("📸 Initial state captured.")
        
        # 2. Minimize a window to trigger a snapshot
        # For simplicity, we'll click the first minimize button we find
        minimize_btns = driver.find_elements(By.CLASS_NAME, "btn-minimize")
        if minimize_btns:
            print(f"📉 Minimizing {len(minimize_btns)} windows to trigger snapshots...")
            for btn in minimize_btns[:3]: # Just do 3 for testing
                btn.click()
                time.sleep(1) # Wait for snapshot logic
        
        # 3. Hover over taskbar items and check for snapshot-img
        taskbar_icons = driver.find_elements(By.CLASS_NAME, "taskbar-icon")
        actions = ActionChains(driver)
        
        snapshot_found = False
        for i, icon in enumerate(taskbar_icons):
            actions.move_to_element(icon).perform()
            time.sleep(0.5) # Wait for hover preview delay
            
            # Check if preview shows a snapshot image
            try:
                snapshot = driver.find_element(By.CLASS_NAME, "snapshot-img")
                print(f"✅ Found snapshot image for Taskbar Icon {i}")
                snapshot_found = True
                
                # Capture the preview
                driver.save_screenshot(f"taskbar_preview_{i}.png")
            except:
                # If no snapshot, maybe it just shows the fake content
                print(f"ℹ️ Taskbar Icon {i} showing skeleton content or no preview.")
        
        if snapshot_found:
            print("\n========================================")
            print("🎉 TASKBAR SNAPSHOTS VERIFIED")
            print("========================================")
        else:
            print("\n❌ Taskbar snapshots not found. Check if html2canvas and hook are working.")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_taskbar_snapshots()
