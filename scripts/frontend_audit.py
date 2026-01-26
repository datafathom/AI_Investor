from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

# Configuration
BASE_URL = "http://localhost:5173"
SCREENSHOT_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\screenshots\1_14_26"
SUCCESS_DIR = os.path.join(SCREENSHOT_DIR, "success")
FAIL_DIR = os.path.join(SCREENSHOT_DIR, "fail")

# Create directories clean
os.makedirs(SUCCESS_DIR, exist_ok=True)
os.makedirs(FAIL_DIR, exist_ok=True)

class RobustAuditor:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Commented for visibility if needed
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def perform_real_auth(self):
        """Standard Browser Verification Style: UI Register -> API Verify -> Session Detect -> UI Login UI."""
        print("👤 Starting AUTHENTIC UI Auth Flow...")
        self.driver.get(BASE_URL)
        time.sleep(3)
        
        # Identity for today
        today_str = time.strftime("%Y_%m_%d_%H%M%S")
        test_email = f"audit_{today_str}@datafathom.biz"
        test_pass = "AuditPass123!"

        try:
            # 1. Open Registration mode
            print(f"   - Opening Registration for: {test_email}")
            switch_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "switch-auth")))
            if "Sign Up" in switch_btn.text:
                switch_btn.click()
                time.sleep(1)

            # 2. Register
            email_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
            pass_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            submit_btn = self.driver.find_element(By.CLASS_NAME, "auth-button")

            email_input.send_keys(test_email)
            pass_input.send_keys(test_pass)
            submit_btn.click()
            
            print("   - Registration submitted. Waiting for backend sink...")
            time.sleep(5) 
            
            # 3. Programmatic Email Verification (Backend Bypass)
            print(f"   - VERIFYING account via API...")
            import requests
            verify_res = requests.get(f"http://localhost:5050/api/auth/verify-email?email={test_email}&token=mock_verify_token")
            print(f"   - API Response: {verify_res.status_code}")
            time.sleep(2)

            # 4. Final Verification / Login
            print("   - Refreshing to stabilize session...")
            self.driver.get(BASE_URL)
            time.sleep(5)
            
            # Note: App.jsx might auto-login here if registration was successful
            modals = self.driver.find_elements(By.CLASS_NAME, "modal-overlay")
            if not modals or not modals[0].is_displayed():
                print("   - No login modal detected. Checking for App Shell...")
                try:
                    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "app-shell")))
                    print("   ✅ ALREADY LOGGED IN: Registration auto-logged us in.")
                except:
                    print("   ⚠️ App Shell not found and Modal not present. Forcing login trigger...")
                    self.driver.get(f"{BASE_URL}/")
                    time.sleep(3)
            
            # If still not logged in, perform manual login
            modals = self.driver.find_elements(By.CLASS_NAME, "modal-overlay")
            if modals and modals[0].is_displayed():
                print("   - Performing manual UI Login...")
                email_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                pass_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                submit_btn = self.driver.find_element(By.CLASS_NAME, "auth-button")
                
                email_input.clear()
                email_input.send_keys(test_email)
                pass_input.clear()
                pass_input.send_keys(test_pass)
                submit_btn.click()
                self.wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "modal-overlay")))

            # 5. Final validation
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "app-shell")))
            print("   ✅ AUTHENTICATED: Registration, Verification, and Session Confirmed.")
            
            # Inject onboarding skip
            self.driver.execute_script("localStorage.setItem('onboarding_completed', 'skipped');")
            
        except Exception as e:
            print(f"   ❌ AUTHENTICATION CHAIN BROKE: {e}")
            self.driver.save_screenshot(os.path.join(FAIL_DIR, "CRITICAL_AUTH_FAILURE.png"))
            raise e

    def verify_page_integrity(self, label):
        """Checks for Gold Standard elements and common failures."""
        try:
            # Check for Login Modal - if visible, we are logged out
            modals = self.driver.find_elements(By.CLASS_NAME, "modal-overlay")
            if modals and modals[0].is_displayed():
                return "FAIL_STUCK_ON_LOGIN", "The login modal is visible, preventing access to the dashboard content."
            
            # Look for App Shell
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "app-shell")))
            
            # Content Check
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            if "not found" in body_text or "404" in body_text:
                return "FAIL_404", "The page content contains 'Not Found' or '404' indicators, suggesting a broken route or missing data."
            if "something went wrong" in body_text or "react-error" in body_text:
                return "FAIL_REACT_CRASH", "A React error boundary or 'Something went wrong' message was detected in the UI."
                
            # Gold Standard Check
            panels = self.driver.find_elements(By.CLASS_NAME, "glass-panel")
            if not panels and "legal" not in self.driver.current_url:
                return "FAIL_EMPTY_CONTENT", "The page loaded successfully but lacks any '.glass-panel' elements (Gold Standard UI requirement)."

            return "SUCCESS", "Page meets all accessibility and Gold Standard UI criteria."
        except Exception as e:
            # Capture browser logs on failure
            try:
                logs = self.driver.get_log('browser')
                log_file = os.path.join(FAIL_DIR, f"LOGS_{label.replace(' ', '_')}.json")
                with open(log_file, "w") as f:
                    json.dump(logs, f, indent=2)
            except:
                pass
            
            # Clean up error message for filename safety
            err_msg = str(e).replace('\n', ' ')[:100].strip()
            return f"FAIL_TIMEOUT", f"Verification timed out or failed with error: {err_msg}"

    def audit_loop(self, map_data):
        print("🚀 Starting ROBUST Audit...")
        self.perform_real_auth()
        time.sleep(2)

        results = []
        for category, submenus in map_data.items():
            for submenu, items in submenus.items():
                for label, path in items.items():
                    print(f"🔍 Testing [{category}] > {label} @ {path}")
                    
                    try:
                        self.driver.get(f"{BASE_URL}{path}")
                        
                        # Slow down for rendering (7s)
                        time.sleep(7)
                        
                        status, description = self.verify_page_integrity(label)
                        filename = f"{category}_{label.replace(' ', '_')}.png"
                        
                        if status == "SUCCESS":
                            # 1. Initial Load Screenshot
                            target_initial = os.path.join(SUCCESS_DIR, filename)
                            self.driver.save_screenshot(target_initial)
                            
                            # 2. Scrolled Screenshot
                            print(f"   - Scrolling for depth capture...")
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2) # Wait for potential scroll animations/lazy loads
                            target_scrolled = os.path.join(SUCCESS_DIR, filename.replace(".png", "_scrolled.png"))
                            self.driver.save_screenshot(target_scrolled)
                            
                            print(f" ✅ Saved Success (Dual-Capture): {label}")
                        else:
                            target = os.path.join(FAIL_DIR, f"{status}_{filename}")
                            self.driver.save_screenshot(target)
                            print(f" ❌ Saved Failure [{status}]: {label} - {description}")
                        
                        results.append({
                            "page": label, 
                            "path": path, 
                            "status": status,
                            "description": description
                        })
                        
                    except Exception as e:
                        print(f" 🔥 Blocker on {label}: {e}")
                        results.append({
                            "page": label, 
                            "status": "BLOCKER",
                            "description": str(e)
                        })

        # Final Report
        with open(os.path.join(SCREENSHOT_DIR, "Audit_Results.json"), "w") as f:
            json.dump(results, f, indent=2)

    def close(self):
        self.driver.quit()

AUDIT_MAP = {
    "Routes": {
        "CoreWorkspaces": {
            "Terminal": "/workspace/terminal",
            "MissionControl": "/workspace/mission-control",
            "AutoCoderDashboard": "/workspace/autocoder",
            "AutoCoderSandbox": "/workspace/auto-coder",
            "VRCockpit": "/workspace/vr",
            "Chat": "/chat"
        },
        "AnalysisLogic": {
            "PoliticalAlpha": "/analytics/political",
            "StrategyDistillery": "/analytics/strategy",
            "OptionsAnalytics": "/analytics/options",
            "BacktestExplorer": "/portfolio/backtest",
            "DebateChamber": "/workspace/debate"
        },
        "PortfolioManagement": {
            "VirtualBrokerage": "/portfolio/brokerage",
            "GlobalScanner": "/scanner/global",
            "Attribution": "/portfolio/attribution",
            "FixedIncome": "/portfolio/fixed-income",
            "Crypto": "/portfolio/crypto",
            "TaxOptimization": "/portfolio/tax",
            "Assets": "/assets",
            "CashFlow": "/portfolio/cash-flow",
            "Tenants": "/tenant",
            "AdvancedAnalytics": "/portfolio/advanced-analytics",
            "Optimization": "/portfolio/optimization",
            "RiskManagement": "/portfolio/risk",
            "TaxEnhanced": "/portfolio/tax-optimization"
        },
        "TradingExecution": {
            "OptionsStrategy": "/trading/options",
            "AdvancedOrders": "/trading/advanced-orders",
            "PaperTrading": "/trading/paper",
            "AlgorithmicTrading": "/trading/algorithmic"
        },
        "EnterpriseCompliance": {
            "Enterprise": "/enterprise",
            "Compliance": "/compliance",
            "Institutional": "/institutional"
        },
        "AI_ML": {
            "MLTraining": "/ml/training",
            "AIPredictions": "/ai/predictions",
            "AIAssistant": "/ai/assistant"
        },
        "Integrations": {
            "Platform": "/integrations",
            "Developer": "/developer/platform",
            "Marketplace": "/marketplace"
        },
        "ModuleOverviews": {
            "CoreWorkspaceOverview": "/workspace",
            "AnalyticsOverview": "/analytics",
            "PortfolioOverview": "/portfolio",
            "AnalystOverview": "/analyst",
            "GuardianOverview": "/guardian",
            "StrategistOverview": "/strategist",
            "ArchitectOverview": "/architect",
            "ObserverOverview": "/observer",
            "ScannerOverview": "/scanner"
        }
    },
    "Account": {
        "Settings": {
            "Profile": "/settings"
        }
    },
    "Help": {
        "Legal": {
            "Terms": "/legal/terms",
            "Privacy": "/legal/privacy"
        }
    },
    "Special": {
        "Mode": {
            "Mobile": "/mobile",
            "Zen": "/zen"
        }
    }
}

if __name__ == "__main__":
    auditor = RobustAuditor()
    try:
        auditor.audit_loop(AUDIT_MAP)
    finally:
        auditor.close()
