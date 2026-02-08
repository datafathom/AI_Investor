import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def capture_admin_pages():
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Run in headless mode to avoid window popping up
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    pages = {
        "admin_health": "http://localhost:5173/admin/health",
        "admin_performance": "http://localhost:5173/admin/performance",
        "admin_middleware": "http://localhost:5173/admin/middleware",
        "admin_alerts": "http://localhost:5173/admin/alerts"
    }
    
    screenshot_dir = os.path.join(os.getcwd(), "screenshots", "phase2_verification")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    try:
        for name, url in pages.items():
            print(f"Navigating to {url}...")
            driver.get(url)
            # Wait for any loading states to clear
            time.sleep(5) 
            
            # Simple check for login redirect
            if "login" in driver.current_url.lower():
                print(f"⚠️ Redirected to login at {driver.current_url}. Authentication might be required.")
                # We could try to login here if we had credentials, 
                # but for dev usually we bypass or have a test user.
            
            path = os.path.join(screenshot_dir, f"{name}.png")
            driver.save_screenshot(path)
            print(f"✅ Saved screenshot: {path}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_admin_pages()
