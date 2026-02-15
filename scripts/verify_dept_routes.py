import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_routes():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # 1. Login
        driver.get("http://localhost:5173/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        
        # Adjust selectors based on your LoginModal implementation
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("password123") # Assuming default or mocked
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()
        
        time.sleep(2) # Wait for login
        
        # 2. Check Routes
        test_paths = [
            "/dept/orchestrator",
            "/dept/data-scientist",
            "/dept/banker",
            "/data-scientist/forced-sellers", # Explicit route
            "/architect/goals", # Dynamic workstation
        ]
        
        for path in test_paths:
            print(f"Testing path: {path}")
            driver.get(f"http://localhost:5173{path}")
            time.sleep(1)
            
            # Check for error indicators
            if "WORKSTATION_NOT_FOUND" in driver.page_source:
                print(f"FAILED: Workstation not found for {path}")
            elif "404: Node Missing" in driver.page_source:
                print(f"FAILED: 404 for {path}")
            else:
                print(f"SUCCESS: Loaded {path}")
                
        # 4. Take a screenshot
        driver.save_screenshot("route_verification.png")
        print("Screenshot saved to route_verification.png")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_routes()
