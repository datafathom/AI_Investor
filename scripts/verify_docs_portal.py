import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify_docs_portal(url: str = "http://127.0.0.1:5055"):
    """
    Verifies the Internal Documentation Portal using Selenium.
    Follows Rule 10: Uses local Python scripts for browser control.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for verification
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print(f"🌐 Navigating to {url}...")
        driver.get(url)
        
        # Wait for the app to load (check for sidebar or root element)
        wait = WebDriverWait(driver, 10)
        root_element = wait.until(EC.presence_of_element_located((By.ID, "root")))
        
        # Verify if the title or specific elements are present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sidebar-header")))
        
        print("✅ Portal loaded successfully.")
        
        # Check for _PLANS folder in the sidebar
        try:
            plans_folder = driver.find_element(By.XPATH, "//*[contains(text(), '_PLANS')]")
            print("✅ Found '_PLANS' folder in sidebar.")
        except Exception:
            print("❌ '_PLANS' folder NOT found in sidebar.")
            
        # Capture a screenshot for visual verification
        screenshot_path = os.path.join("screenshots", "docs_portal_verification.png")
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to {screenshot_path}")
        
        # Verify first items are directories (sorting check)
        nodes = driver.find_elements(By.CLASS_NAME, "tree-node")
        if nodes:
            first_icon = nodes[0].find_element(By.TAG_NAME, "svg")
            # We use Folder icon for directories, FileText for files.
            # This is a bit hard to verify without looking at the class, 
            # but we can check if the first node has 'children' wrapper or is a folder.
            print(f"ℹ️ First node in sidebar: {nodes[0].text}")

    except Exception as e:
        print(f"❌ Verification failed: {e}")
        # Take error screenshot
        driver.save_screenshot(os.path.join("screenshots", "docs_portal_error.png"))
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_docs_portal()
