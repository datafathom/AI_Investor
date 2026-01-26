import requests
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Settings
BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:5050/api/v1"
VERIFY_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\screenshots\verify_batch3"
os.makedirs(VERIFY_DIR, exist_ok=True)

def verify_endpoints():
    print("📡 Verifying Backend Endpoints...")
    endpoints = [
        "/brokerage/status",
        "/brokerage/positions",
        "/scanner/matches",
        "/scanner/galaxy",
        "/scanner/pulse"
    ]
    
    for ep in endpoints:
        try:
            res = requests.get(f"{API_URL}{ep}")
            print(f"  [{res.status_code}] {ep}")
            if res.status_code != 200:
                print(f"    ⚠️ Warning: {ep} returned non-200")
        except Exception as e:
            print(f"  [ERR] {ep}: {e}")

def capture_ui():
    print("🖥️  Capturing UI Screenshots...")
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get(BASE_URL)
        time.sleep(5)
        
        # Check for Login
        modals = driver.find_elements(By.CLASS_NAME, "modal-overlay")
        if modals and modals[0].is_displayed():
            print("  🔑 Login Modal detected. Please login or check auth script.")
            # Note: For verification, we assume the user might be logged in or we use a session
            # For now, let's just attempt to bypass or skip if possible
        
        routes = {
            "Terminal": "/workspace/terminal",
            "Brokerage": "/portfolio/brokerage",
            "Scanner": "/scanner/global"
        }
        
        for name, path in routes.items():
            print(f"  📸 Capturing {name} @ {path}...")
            driver.get(f"{BASE_URL}{path}")
            time.sleep(10) # Heavy rendering time
            
            # Diagnostic check for 404 content
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            if "not found" in body_text or "404" in body_text:
                print(f"    ❌ FAIL: {name} shows 404 indicators in body text!")
            
            driver.save_screenshot(os.path.join(VERIFY_DIR, f"{name}.png"))
            
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_endpoints()
    capture_ui()
