import time
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service

# Configuration
BASE_URL = "http://127.0.0.1:5173"
SCREENSHOT_DIR = r"C:\Users\astir\.gemini\antigravity\brain\c6067579-5907-4fb6-9f0e-774b292fca7b"
PAGES = {
    "ops_dashboard": "/admin/ops",
    "workspace_manager": "/admin/workspaces",
    "environment_settings": "/admin/env",
    "feature_flags": "/admin/features"
}

def capture_screenshots():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    try:
        # 1. Initial load to set bypass
        print(f"Loading {BASE_URL} to apply bypass...")
        driver.get(BASE_URL)
        time.sleep(2)
        driver.execute_script("localStorage.setItem('widget_os_bypass', 'true');")
        driver.refresh()
        time.sleep(3)
        
        for name, path in PAGES.items():
            url = f"{BASE_URL}{path}"
            print(f"Capturing {name} from {url}...")
            driver.get(url)
            
            # Wait for content to load
            try:
                # Wait for a common element in admin pages, or just sleep
                time.sleep(5) 
                
                shot_path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
                driver.save_screenshot(shot_path)
                print(f"✅ Saved: {shot_path}")
            except Exception as e:
                print(f"❌ Failed to capture {name}: {e}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    capture_screenshots()
