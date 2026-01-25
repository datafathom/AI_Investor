import time
import os
import sys
from playwright.sync_api import sync_playwright

# Ensure screenshots directory exists
SCREENSHOT_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\screenshots\Almost_Prod_Ready"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

ROUTES = [
    "/workspace/terminal",
    "/workspace/mission-control",
    "/analytics/political",
    "/analytics/strategy",
    "/workspace/debate",
    "/workspace/autocoder",
    "/workspace/vr",
    "/analytics/options",
    "/analyst/backtest",
    "/strategist/estate",
    "/strategist/impact",
    "/strategist/corporate",
    "/architect/system",
    "/architect/api",
    "/guardian/compliance/audit",
    "/guardian/scenarios",
    "/guardian/margin",
    "/mobile",
    "/portfolio/brokerage",
    "/workspace/auto-coder",
    "/portfolio/attribution",
    "/portfolio/fixed-income",
    "/portfolio/crypto",
    "/portfolio/tax",
    "/observer/macro",
    "/guardian/compliance",
    "/analyst/debate",
    "/strategist/currency",
    "/scanner/global",
    "/assets",
    "/portfolio/cash-flow",
    "/zen",
    "/tenant",
    "/portfolio/advanced-analytics",
    "/portfolio/optimization",
    "/portfolio/risk",
    "/portfolio/tax-optimization",
    "/planning/financial",
    "/planning/retirement",
    "/budgeting",
    "/trading/options",
    "/trading/paper",
    "/trading/algorithmic",
    "/planning/estate",
    "/billing/payments",
    "/credit/monitoring",
    "/research/reports",
    "/social/trading",
    "/community/forums",
    "/education",
    "/charting/advanced",
    "/trading/advanced-orders",
    "/enterprise",
    "/compliance",
    "/institutional",
    "/ml/training",
    "/integrations",
    "/developer/platform",
    "/marketplace",
    "/news/sentiment",
    "/watchlists/alerts",
    "/ai/predictions",
    "/ai/assistant",
    "/legal/terms",
    "/legal/privacy",
    "/settings"
]

def verify():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        print("Navigating to login...")
        try:
            page.goto("http://localhost:5173", timeout=60000)
        except Exception as e:
            print(f"Failed to load localhost:5173: {e}")
            return

        # Attempt Login
        try:
            # Check if login modal is visible (wait a bit)
            try:
                page.wait_for_selector(".auth-modal", timeout=5000)
                print("Login modal detected. Logging in...")
                
                page.fill("input[type='text']", "admin")
                page.fill("input[type='password']", "password123")
                page.click("button[type='submit']")
                
                # Wait for modal to disappear
                page.wait_for_selector(".auth-modal", state="hidden", timeout=10000)
                print("Login successful (modal closed).")
            except:
                print("Login modal not found or already logged in.")
            
        except Exception as e:
            print(f"Login flow warning: {e}")

        # Verification Loop
        for route in ROUTES:
            full_url = f"http://localhost:5173{route}"
            print(f"Verifying {route}...")
            try:
                page.goto(full_url, wait_until="networkidle", timeout=30000)
                time.sleep(2) # Animation buffer
                
                # Check for error boundary text
                content = page.content()
                if "Something went wrong" in content or "Runtime Error" in content:
                    print(f"FAILURE on {route}: Error detected in page content.")
                    continue
                
                # Screenshot
                safe_name = route.replace("/", "_").strip("_")
                if not safe_name: safe_name = "root"
                path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
                page.screenshot(path=path)
                print(f"SUCCESS: {route}")
                
            except Exception as e:
                print(f"FAILURE on {route}: {e}")

        browser.close()

if __name__ == "__main__":
    verify()
