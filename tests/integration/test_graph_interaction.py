import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def test_graph_interaction():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20)
    
    try:
        # 1. Login
        driver.get("http://localhost:5173/login")
        print("Navigated to login")
        
        # Try to find email input
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.clear()
        email_input.send_keys("demo@aiinvestor.com")
        
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pass_input.clear()
        pass_input.send_keys("investor_password")
        
        # Updated selector for login button
        login_btn = driver.find_element(By.CSS_SELECTOR, "button.auth-button")
        login_btn.click()
        print("Login clicked")
        
        # 2. Wait for redirect and navigate to Orchestrator
        time.sleep(3)
        driver.get("http://localhost:5173/orchestrator")
        print("Navigated to Orchestrator")
        
        # 3. Verify Graph Canvas / Main Content
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "orchestrator-dashboard-container")))
        print("Orchestrator dashboard container detected")
        
        # 4. Verify Widgets
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Neo4j Super-Graph')]")))
        print("Graph Title detected")
        
        # 5. Take Screenshot
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot("screenshots/master_orchestrator_verification_final.png")
        print("Screenshot saved to screenshots/master_orchestrator_verification_final.png")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        driver.save_screenshot("screenshots/test_failure.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_graph_interaction()
