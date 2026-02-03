
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def debug_ui():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "http://localhost:5173"
        print(f"Navigating to {url}")
        driver.get(url)
        time.sleep(10) # 10 seconds for full load
        
        # Save screenshot
        driver.save_screenshot("debug_homepage.png")
        print("Saved debug_homepage.png")
        
        # Print body HTML partially
        body_html = driver.find_element("tag name", "body").get_attribute("outerHTML")
        with open("debug_body.html", "w", encoding="utf-8") as f:
            f.write(body_html)
        print("Saved debug_body.html")
        
        # Look for 'Account' or 'Login' strings
        if "Account" in body_html:
            print("Found 'Account' in HTML")
        if "Login" in body_html:
            print("Found 'Login' in HTML")
        if "Sign In" in body_html:
            print("Found 'Sign In' in HTML")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_ui()
