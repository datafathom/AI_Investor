import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_workstations():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("Connecting to Missions Board...")
        driver.get("http://localhost:5173/special/missions")
        time.sleep(3)
        
        # Take screenshot of Missions Board
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots/missions_board_expanded.png")
        print("Missions Board screenshot saved.")

        # Check for new roles
        roles_to_check = ["Auditor", "Envoy", "Hunter", "Physicist", "Steward"]
        for role in roles_to_check:
            try:
                element = driver.find_element(By.XPATH, f"//*[contains(text(), '{role}')]")
                print(f"Verified role presence: {role}")
            except:
                print(f"FAILED to find role: {role}")

        # Try a dynamic route
        # /strategist/builder
        print("Checking dynamic route: /strategist/builder")
        driver.get("http://localhost:5173/strategist/builder")
        time.sleep(3)
        driver.save_screenshot("screenshots/workstation_strategist_builder.png")
        
        if "STRATEGY BUILDER" in driver.page_source.upper():
            print("Verified Dynamic Workstation: Strategy Builder")
        else:
            print("FAILED to verify Strategy Builder workstation")

        # Try another one: /trader/monitor
        print("Checking dynamic route: /trader/monitor")
        driver.get("http://localhost:5173/trader/monitor")
        time.sleep(3)
        driver.save_screenshot("screenshots/workstation_trader_monitor.png")
        
        if "MARKET MONITOR" in driver.page_source.upper():
            print("Verified Dynamic Workstation: Market Monitor")
        else:
            print("FAILED to verify Market Monitor workstation")

    finally:
        driver.quit()

if __name__ == "__main__":
    verify_workstations()
