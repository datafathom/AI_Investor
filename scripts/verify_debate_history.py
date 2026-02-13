
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def verify_debate_history():
    print("Starting verification for Debate History Route...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 1. Navigate to the page
        url = "http://localhost:5173/data-scientist/debate-history"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # 2. Wait for page to load and check title or unique element
        # The page has "Debate History" in h1
        print("Waiting for page content...")
        try:
            h1_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Debate History')]"))
            )
            print("âœ… Page Title Found: Debate History")
        except Exception as e:
            print(f"âŒ Failed to find Page Title: {e}")
            driver.save_screenshot("debug_debate_history_fail.png")
            return False

        # 3. Check for list of history items
        try:
            # The list items have tickers like NVDA, TSLA etc.
            # We can look for the container or specific text
            list_container = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".overflow-y-auto"))
            )
            print("âœ… History List Container Found")
            
            # Check for at least one item
            items = list_container.find_elements(By.CSS_SELECTOR, ".cursor-pointer")
            if len(items) > 0:
                print(f"âœ… Found {len(items)} debate history items.")
            else:
                print("âš ï¸ Warning: History list is empty.")
                
        except Exception as e:
            print(f"âŒ Failed to find history items: {e}")
            return False

        # 4. Take a success screenshot
        driver.save_screenshot("verify_debate_history_success.png")
        print("âœ… Verification Screenshot saved: verify_debate_history_success.png")
        
        return True

    except Exception as e:
        print(f"âŒ Verification Failed with error: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    success = verify_debate_history()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
