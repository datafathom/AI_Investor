from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def test_chrome_driver():
    print("🚀 Initializing Chrome Driver...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode for verification
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        url = "http://localhost:5173"
        print(f"🌍 Navigating to {url}...")
        driver.get(url)
        
        time.sleep(5)  # Wait for page load
        
        screenshot_path = os.path.abspath("selenium_verify_screenshot.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")
        
        print(f"📖 Page Title: {driver.title}")
        
        driver.quit()
        print("✅ Chrome Driver Test SUCCESSFUL")
        return True
    except Exception as e:
        print(f"❌ Chrome Driver Test FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_chrome_driver()
