import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def verify_institutional_routes():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Run in headless for CI/Verification
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Base URL - trying localhost first (might be IPv6 ::1)
    base_url = "http://localhost:5173"
    
    # Simple check if reachable, else fallback
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(("127.0.0.1", 5173))
        base_url = "http://127.0.0.1:5173"
        print("Connected via IPv4 127.0.0.1")
    except:
        print("Falling back to localhost (IPv6 ::1?)")
        base_url = "http://localhost:5173"
    finally:
        s.close()
    
    routes = [
        "/orchestrator",
        "/strategist/scm",
        "/sentinel/strategy",
        "/research/reports"
    ]
    
    results = {}

    try:
        # 1. Login first
        print(f"Navigating to {base_url}/login for authentication...")
        driver.get(f"{base_url}/login")
        time.sleep(2)
        
        try:
            # Wait for modal or login fields
            print("Looking for login modal...")
            # The modal might take a second to fade in
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_field = driver.find_element(By.NAME, "password")
            # The button might be selected by class if type=submit is used by others
            login_button = driver.find_element(By.CSS_SELECTOR, "button.auth-button")
            
            username_field.send_keys("admin") # Username 'admin' from seed
            password_field.send_keys("admin") # Password 'admin' -> hash 'mock_hash_nimda'
            login_button.click()
            
            print("Login submitted. Waiting for redirection...")
            time.sleep(5)
        except Exception as e:
            print(f"Login form not found or already logged in: {e}")
        
        for route in routes:
            url = f"{base_url}{route}"
            print(f"Verifying {url}...")
            driver.get(url)
            
            # Wait for route content
            time.sleep(5) # Give it time to load/render
            
            # Capture screenshot
            screenshot_path = f"screenshots/verify_{route.replace('/', '_')}.png"
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(screenshot_path)
            
            # Check for crash (White screen / No elements)
            try:
                # Find a common element like 'main'
                main_found = driver.find_elements(By.CSS_SELECTOR, "main")
                results[route] = {
                    "loaded": len(main_found) > 0,
                    "screenshot": screenshot_path,
                    "url": driver.current_url
                }
                
                # Check for "lazy load error" or React crash in console
                logs = driver.get_log("browser")
                results[route]["errors"] = logs # Capture all logs
                
            except Exception as e:
                results[route] = {"error": str(e)}

        print("\n--- VERIFICATION RESULTS ---")
        for route, data in results.items():
            status = "LOADED" if data.get("loaded") else "FAILED"
            log_count = len(data.get("errors", []))
            print(f"{route}: {status} | Logs: {log_count} | At: {data.get('url')}")
            if log_count > 0:
                for entry in data["errors"]:
                    # Clean up messages that might contain problematic characters
                    msg = entry['message'].encode('ascii', 'ignore').decode('ascii')
                    print(f"  [{entry['level']}] {msg}")

    finally:
        driver.quit()

if __name__ == "__main__":
    verify_institutional_routes()
