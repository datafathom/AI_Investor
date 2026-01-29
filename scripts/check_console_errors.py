import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def check_console_errors():
    print("🚀 Checking for console errors...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Enable logging
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("http://localhost:5173")
        time.sleep(5) 
        
        print("\n--- BROWSER CONSOLE LOGS ---")
        for entry in driver.get_log('browser'):
            print(entry)
        
        driver.save_screenshot("debug_after_fix.png")
        print("\n📸 Screenshot saved to debug_after_fix.png")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    check_console_errors()
