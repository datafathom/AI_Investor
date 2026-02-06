import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def capture_phase_7_verification():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Base URL
        base_url = "http://localhost:5173"
        print(f"Connecting to {base_url}...")
        
        # 1. Fleet Dashboard
        driver.get(f"{base_url}/special/fleet")
        time.sleep(3) # Wait for animations
        fleet_path = os.path.abspath("phase_7_fleet_dashboard.png")
        driver.save_screenshot(fleet_path)
        print(f"Captured Fleet Dashboard: {fleet_path}")
        
        # 2. Logic Forge (IDE)
        driver.get(f"{base_url}/architect/dev-platform")
        time.sleep(3)
        ide_path = os.path.abspath("phase_7_logic_forge.png")
        driver.save_screenshot(ide_path)
        print(f"Captured Logic Forge: {ide_path}")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_phase_7_verification()
