import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_navigation():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Base URL
        url = "http://localhost:5173"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Bypass Auth Modal for testing
        print("Setting bypass in local storage...")
        driver.execute_script("localStorage.setItem('widget_os_bypass', 'true');")
        driver.refresh()
        
        # Wait for the app to load
        wait = WebDriverWait(driver, 10)
        
        # Verify if we are on the dashboard
        print("Waiting for any dashboard element...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Take a screenshot of the home page
        time.sleep(5)
        os.makedirs("scripts/screenshots", exist_ok=True)
        driver.save_screenshot("scripts/screenshots/dashboard_home.png")
        print("Screenshot saved to scripts/screenshots/dashboard_home.png")

        # Test specific routes
        routes_to_test = [
            "/dept/data-scientist",
            "/data-scientist/forced-sellers",
            "/data-scientist/whale-flow",
            "/data-scientist/research",
            "/dept/architect",
            "/architect/goals"
        ]
        
        for route in routes_to_test:
            print(f"Testing route: {route}")
            driver.get(f"{url}{route}")
            time.sleep(3)
            
            # Check for "Node Missing" or "ERROR"
            page_text = driver.find_element(By.TAG_NAME, "body").text
            if "Node Missing" in page_text or "ERROR: WORKSTATION_NOT_FOUND" in page_text:
                print(f"FAILED: Route {route} is broken (404 or Workstation Not Found).")
            elif "ERROR" in page_text.upper() and len(page_text) < 1000: # Simple error check
                 print(f"FAILED: Route {route} shows an error page.")
            else:
                print(f"SUCCESS: Route {route} appears to load.")
                driver.save_screenshot(f"scripts/screenshots/route_{route.replace('/', '_')}.png")

    except Exception as e:
        print(f"An error occurred during verification: {e}")
        driver.save_screenshot("scripts/screenshots/error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_navigation()
