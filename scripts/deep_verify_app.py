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
    print("Initializing Deep Verification (With Auth Bypass)...")
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
            """
        })
        
        # Navigate to set domain context
        driver.get(base_url)
        time.sleep(5)
        
        # Navigate to Strategy Page
        strategy_url = f"{base_url}/analytics/strategy"
        print(f"Navigating to {strategy_url}...")
        driver.get(strategy_url)
        time.sleep(5)

        # FORCE HIDE MODAL AFTER NAVIGATION
        print("Force-hiding login modal overlay...")
        driver.execute_script("""
            const hideModal = () => {
                const modal = document.querySelector('.modal-overlay');
                if (modal) {
                    modal.style.display = 'none';
                    console.log('MODAL HIDDEN');
                }
                const authModal = document.querySelector('.auth-modal');
                if (authModal) {
                    authModal.style.display = 'none';
                }
            };
            hideModal();
            // Also run it periodically in case it re-renders
            setInterval(hideModal, 500);
        """)
        
        time.sleep(5) # Wait for content to render under the hidden modal

        # Check for Strategy Content
        print("Verifying Strategy Content...")
        try:
            canvases = driver.find_elements(By.TAG_NAME, "canvas")
            if canvases:
                print(f"SUCCESS: Found {len(canvases)} Canvas element(s).")
            else:
                print("WARNING: No canvas found on Strategy page.")

            stability_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'TESTING STABILITY')]")
            if stability_text:
                print("SUCCESS: 'TESTING STABILITY' text found in 3D overlay.")
            
        except Exception as e:
            print(f"Content verification failed: {e}")

        # Final Logs Audit
        print("\n--- BROWSER CONSOLE LOGS ---")
        logs = driver.get_log('browser')
        for entry in logs:
            if entry['level'] == 'SEVERE':
                 print(f"[{entry['level']}] {entry['message']}")
        print("--- END LOGS ---\n")

        screenshot_path = os.path.abspath("deep_strategy_verification.png")
        driver.save_screenshot(screenshot_path)
        print(f"Deep verification screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    deep_verify()
