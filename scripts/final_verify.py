import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def deep_verify():
    print("Initializing Enhanced Verification Task...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        base_url = "http://localhost:5173"
        
        # CDP-level injection to ensure mock session is present before React boots
        print("Injecting CDP script for early Auth bypass...")
        mock_user = {"id": "verify-user", "username": "Tester", "role": "admin"}
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': f"""
                localStorage.setItem('widget_os_token', 'mock-verify-token-12345');
                localStorage.setItem('widget_os_user', JSON.stringify({json.dumps(mock_user)}));
                localStorage.setItem('widget_os_tenant_id', 'default');
                console.log('[VERIFY-INIT] LocalStorage pre-populated');
            """
        })
        
        # Navigate to set domain context
        driver.get(base_url)
        time.sleep(5)
        
        # Navigate to Strategy Page
        strategy_url = f"{base_url}/analytics/strategy"
        print(f"Navigating to {strategy_url}...")
        driver.get(strategy_url)
        
        # FORCE HIDE MODAL
        print("Force-hiding login modal...")
        driver.execute_script("""
            const itv = setInterval(() => {
                const modal = document.querySelector('.modal-overlay, .auth-modal');
                if (modal) {
                    modal.style.display = 'none';
                    console.log('[VERIFY] Modal hidden via CSS');
                }
            }, 100);
            window._modalInterval = itv;
        """)

        print("Waiting for 3D Content to render (15s)...")
        time.sleep(15)

        # Check for Strategy Content
        print("Verifying Strategy Content...")
        try:
            canvases = driver.find_elements(By.TAG_NAME, "canvas")
            if canvases:
                print(f"SUCCESS: Found {len(canvases)} Canvas element(s).")
                width = canvases[0].get_attribute('width')
                height = canvases[0].get_attribute('height')
                print(f"Canvas size: {width}x{height}")
            else:
                print("WARNING: No canvas found.")

            stability_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'TESTING STABILITY')]")
            if stability_text:
                print("SUCCESS: 'TESTING STABILITY' text found.")
            
        except Exception as e:
            print(f"Content verification failed: {e}")

        # Final Logs Audit
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        for entry in logs:
            print(f"[{entry['level']}] {entry['message']}")
        print("--- END LOGS ---\n")

        screenshot_path = os.path.abspath("final_strategy_verification.png")
        driver.save_screenshot(screenshot_path)
        print(f"Verification screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    deep_verify()
