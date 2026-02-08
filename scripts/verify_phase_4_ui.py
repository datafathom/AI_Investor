from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def capture_screens():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    pages = {
        "ForcedSellerMonitor": "http://localhost:5173/data-scientist/forced-sellers",
        "WhaleFlowTerminal": "http://localhost:5173/data-scientist/whale-flow",
        "TechnicalIndicators": "http://localhost:5173/data-scientist/indicators"
    }
    
    output_dir = "artifacts/screenshots"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=== Phase 4 UI Verification ===")
    
    # Login first if needed (assuming auto-login or no-auth for dev)
    # If login is required, we'd need to handle it here. 
    # For now, let's try direct navigation.
    
    for name, url in pages.items():
        print(f"Capturing {name} at {url}...")
        driver.get(url)
        time.sleep(5)  # Wait for data to load
        path = os.path.join(os.getcwd(), output_dir, f"{name}.png")
        driver.save_screenshot(path)
        print(f"  Saved to {path}")
        
    driver.quit()
    print("UI Verification Complete.")

if __name__ == "__main__":
    capture_screens()
