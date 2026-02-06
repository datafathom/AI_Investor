import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def verify_frontend():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    print("🚀 Starting Selenium Chrome Driver...")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "http://localhost:5173"
        print(f"🌐 Navigating to {url}...")
        driver.get(url)
        time.sleep(10)  # Wait for React/Vite to load

        # Check for error indicators
        if "404" in driver.title or "Error" in driver.title:
            print(f"❌ ERROR: Possible page error. Title: {driver.title}")
        
        # Take screenshot
        screenshot_path = os.path.abspath("screenshots/frontend_verify_debug.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")

        # Check for specific elements if possible
        # For now, just print the page title
        print(f"📄 Page Title: {driver.title}")
        
        # Check for core text
        if "AI Investor" in driver.page_source or "Sovereign" in driver.page_source:
             print("✅ Success: Page content seems valid.")
        else:
             print("⚠️ Warning: Could not find 'AI Investor' or 'Sovereign' in page source.")

    except Exception as e:
        print(f"❌ Selenium Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_frontend()
