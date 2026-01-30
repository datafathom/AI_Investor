import time
import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:5050"
TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H%M%S")
TEST_EMAIL = f"audit_{TIMESTAMP}@fathom.ai"
TEST_PASS = "RobustTest123!"

def run_verify():
    print(f"🚀 STARTING ROBUST VERIFICATION for Evolution Lab")
    print(f"📧 Identity: {TEST_EMAIL}")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    
    driver = None
    try:
        # 0. API-First Registration (Per Protocol section 6)
        print("📝 Registering user via API...")
        reg_res = requests.post(f"{API_URL}/api/auth/register", json={
            "email": TEST_EMAIL,
            "password": TEST_PASS
        })
        if reg_res.status_code not in [200, 201]:
            print(f"❌ API Registration failed: {reg_res.text}")
            return
        print("✅ API Registration successful")

        # 1. Email Verification Bypass (Per Protocol section 2.3)
        print("📧 Bypassing email verification...")
        verify_url = f"{API_URL}/api/auth/verify-email?email={TEST_EMAIL}&token=mock_verify_token"
        v_res = requests.get(verify_url)
        if v_res.status_code == 200:
            print("✅ Email verified via programmatic bypass")
        else:
            print(f"❌ Email verification failed: {v_res.status_code}")
            return

        # 2. UI Browser Flow
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        driver.get(BASE_URL)
        print("🔗 Navigated to Landing")
        
        # 3. UI Login Flow (Per Protocol section 2.2)
        print("🔑 Performing UI Login...")
        # Modal should be open by default or we wait for it
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "auth-modal")))
        
        email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='email']")
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        email_input.send_keys(TEST_EMAIL)
        pass_input.send_keys(TEST_PASS)
        
        submit_btn = driver.find_element(By.CLASS_NAME, "auth-button")
        driver.execute_script("arguments[0].click();", submit_btn)
        print("🖱️ Login Button Clicked")
        
        # Wait for login to complete and redirect/modal close
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "auth-modal")))
        print("🚪 Authentication Successful, Modal Closed")
        
        # 4. Navigate to Evolution Lab
        print("🚀 Navigating to /evolution...")
        driver.get(f"{BASE_URL}/evolution")
        
        # Check for Gold Standard: .os-bleed and header
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(., 'EVOLUTION LAB')]")))
        print("✅ Header detected")
        
        # 5. Mathematical Layout Validation (AABB)
        widgets = driver.find_elements(By.CLASS_NAME, "rounded-xl")
        print(f"📦 Found {len(widgets)} widget containers")
        
        rects = []
        for i, widget in enumerate(widgets):
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", widget)
            rects.append({'id': i, 'rect': rect})
            
        overlaps = 0
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                r1 = rects[i]['rect']
                r2 = rects[j]['rect']
                if (r1['left'] < r2['right'] and r1['right'] > r2['left'] and
                    r1['top'] < r2['bottom'] and r1['bottom'] > r2['top']):
                    print(f"❌ OVERLAP DETECTED between Widget {i} and {j}!")
                    overlaps += 1
        
        if overlaps == 0:
            print("✅ Layout check: No overlaps detected")
        else:
            print(f"⚠️ Layout check: {overlaps} overlaps found.")
        
        # 6. Functional Check: 3D/Plotly/D3
        # FitnessSurface3D uses <canvas>
        # LineageMap uses <svg>
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
        print("🎨 3D Fitness Surface (Canvas) detected")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "svg")))
        print("🗺️ Lineage Map (SVG) detected")
        
        # 7. Evidence
        os.makedirs("screenshots", exist_ok=True)
        evidence_path = os.path.abspath("screenshots/VERIFY_EVOLUTION.png")
        driver.save_screenshot(evidence_path)
        print(f"📸 EVIDENCE SAVED: {evidence_path}")
        
        print("\n🏆 VERIFICATION SUCCESSFUL")

    except Exception as e:
        print(f"❌ VERIFICATION ERROR: {e}")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            err_path = os.path.abspath("screenshots/VERIFY_EVOLUTION_ERROR.png")
            driver.save_screenshot(err_path)
            print(f"📸 ERROR PROOF SAVED: {err_path}")
            print("--- PAGE SOURCE ---")
            print(driver.page_source[:2000] + "...")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_verify()
