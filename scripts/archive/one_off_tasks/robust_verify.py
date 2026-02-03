from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configuration
BASE_URL = "http://localhost:5173"

def verify_layout(page_path, filename):
    print(f"\n🔍 VERIFYING: {page_path}")
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Headless is safer for scripts
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 1. Navigation & Inject Bypass
        driver.get(BASE_URL)
        time.sleep(3)
        driver.execute_script("localStorage.setItem('auth_token', 'selenium_token');")
        driver.execute_script("localStorage.setItem('onboarding_completed', 'skipped');")
        
        # 2. Go to Target Page
        target = f"{BASE_URL}{page_path}"
        driver.get(target)
        time.sleep(5) # Wait for RGL to settle
        
        # 3. Find all widget containers
        # Our refactor uses 'overflow-hidden rounded-xl' for the RGL child
        widgets = driver.find_elements(By.CLASS_NAME, "rounded-xl")
        print(f"📦 Found {len(widgets)} widgets.")
        
        rects = []
        for i, widget in enumerate(widgets):
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", widget)
            rects.append({'id': i, 'rect': rect})
            print(f"   Widget {i}: x={rect['left']}, y={rect['top']}, w={rect['width']}, h={rect['height']}")
            
        # 4. Math Check: Overlaps
        overlaps = 0
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                r1 = rects[i]['rect']
                r2 = rects[j]['rect']
                # Standard AABB overlap check
                if (r1['left'] < r2['right'] and r1['right'] > r2['left'] and
                    r1['top'] < r2['bottom'] and r1['bottom'] > r2['top']):
                    print(f"❌ OVERLAP DETECTED between Widget {i} and {j}!")
                    overlaps += 1
        
        if overlaps == 0 and len(widgets) > 0:
            print(f"✅ NO OVERLAPS FOUND for {page_path}")
        else:
            print(f"⚠️ Layout check: {overlaps} overlaps found.")

        # 5. Capture proof
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.abspath(f"screenshots/{filename}")
        driver.save_screenshot(path)
        print(f"📸 PROOF SAVED: {path}")
        
    except Exception as e:
        print(f"❌ Verification ERROR: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    verify_layout("/trading/options", "VERIFY_TRADING_LAYOUT.png")
    verify_layout("/analytics/options", "VERIFY_ANALYTICS_LAYOUT.png")
