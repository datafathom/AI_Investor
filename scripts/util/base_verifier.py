"""
===============================================================================
FILE: scripts/util/base_verifier.py
ROLE: Battle-Hardened Selenium Base Verifier
PURPOSE: Provides a robust framework for frontend verification, including
         session management, console log capture, and error correlation.
===============================================================================
"""

import os
import sys
import time
import logging
import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Constants
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_TIMEOUT = 10
DEBUG_DIR = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit"

class BaseVerifier:
    def __init__(self, headless: bool = False, window_size: str = "1920,1080", dept_name: str = None):
        self.headless = headless
        self.window_size = window_size
        self.dept_name = dept_name
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = self._setup_logger()
        self.session_data: Dict[str, Any] = {}
        
        # Ensure debug directories exist
        self.today_str = datetime.now().strftime("%m_%d_%y")
        
        # Handle dynamic paths based on department
        base_results_dir = DEBUG_DIR / "results"
        
        if self.dept_name:
            # New structure: results/<dept>_results/<dept>_screenshots
            self.results_dir = base_results_dir / f"{self.dept_name}_results"
            self.screenshot_dir = self.results_dir / f"{self.dept_name}_screenshots"
            # JSON filename: <dept>_<date>_verify_results.json
            self.results_filename = f"{self.dept_name}_{self.today_str}_verify_results.json"
        else:
            # Validation fallback / Legacy structure
            self.results_dir = base_results_dir
            self.screenshot_dir = DEBUG_DIR / "Screenshots_FrontEndAudit" / self.today_str
            self.results_filename = f"{self.today_str}_verify_results.json"

        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Tracking for the current session
        self.current_session_screenshots = {
            "SUCCESS": [],
            "FAILED": [],
            "OTHER": []
        }

    def finalize_run(self):
        """
        Cleanup logic based on user rules.
        If there are ANY failures, delete all success screenshots from this run.
        """
        has_failures = len(self.current_session_screenshots["FAILED"]) > 0
        
        # Only clean up if there are actual failures (ignore NOT_IMPLEMENTED/OTHER)
        
        if has_failures:
            self.logger.info("Failures detected in run. Cleaning up SUCCESS screenshots to keep folder focused.")
            for path in self.current_session_screenshots["SUCCESS"]:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                        self.logger.info(f"Deleted success screenshot: {os.path.basename(path)}")
                except Exception as e:
                    self.logger.error(f"Failed to delete {path}: {e}")
        else:
            self.logger.info("No failures detected (or only NOT_IMPLEMENTED). Skipping cleanup. Keeping all success screenshots.")

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def start_driver(self):
        self.logger.info("Initializing Selenium WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument(f"--window-size={self.window_size}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Enable console log capture
        chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_browser_logs(self) -> List[Dict]:
        """Captures browser console logs."""
        try:
            return self.driver.get_log('browser')
        except:
            return []

    def get_backend_logs(self, lines: int = 50) -> List[str]:
        """Tails backend log file."""
        log_path = PROJECT_ROOT / "logs" / "backend_debug.log"
        if not log_path.exists():
            return ["Backend log not found."]
        
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.readlines()[-lines:]
        except Exception as e:
            return [f"Error reading backend logs: {e}"]

    def capture_status(self, status: str, route: str, errors: Optional[List[str]] = None, metadata: Optional[Dict] = None) -> str:
        """
        Takes a screenshot and IMMEDIATELY logs the result to JSON.
        status: SUCCESS, FAILED, ERROR, etc.
        """
        safe_route = route.replace('/', '_').strip('_') or "root"
        timestamp = datetime.now().strftime("%H_%M_%S")
        filename = f"{status.lower()}_{safe_route}_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        
        try:
            self.driver.save_screenshot(str(filepath))
            self.logger.info(f"Screenshot saved: {filename}")
            
            # Clean up errors for readability before logging
            readable_errors = self.clean_console_errors(errors or [])
            
            # Log to JSON immediately
            self.log_result(route, status, readable_errors, str(filepath), metadata)
            
            # Track for cleanup
            status_key = "SUCCESS" if status == "SUCCESS" else ("FAILED" if status in ("FAILED", "ERROR") else "OTHER")
            self.current_session_screenshots[status_key].append(str(filepath))
            
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to save screenshot or log result: {e}")
            return ""

    def clean_console_errors(self, errors: List[str]) -> List[str]:
        """Filters out noisy stacktraces and redundant Selenium/WebDriver junk."""
        cleaned = []
        for err in errors:
            # If it's a massive stacktrace blob, just take the first few lines
            if "Stacktrace:" in err or "Symbols not available" in err:
                lines = err.split('\n')
                # Try to find the actual message
                msg = next((l for l in lines if l.startswith("Message:")), lines[0])
                cleaned.append(msg.strip())
            else:
                cleaned.append(err.strip())
        return cleaned

    def wait_for_page_ready(self, timeout: int = 20) -> bool:
        """
        Robustly waits for the page to be 'ready' by:
        1. Waiting for loading spinners/skeletons to disappear.
        2. Waiting for a main content container to appear and HAVE CHILDREN.
        """
        self.logger.info("Waiting for page-ready state (spinners/skeletons clear)...")
        
        # 1. Wait for spinners/skeletons to GO AWAY
        loaders = [
            (By.CLASS_NAME, "loading-spinner-container"),
            (By.CLASS_NAME, "skeleton-container"),
            (By.CLASS_NAME, "loading-overlay")
        ]
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            active_loaders = []
            for by, selector in loaders:
                try:
                    if self.driver.find_elements(by, selector):
                        active_loaders.append(selector)
                except:
                    continue
            
            if not active_loaders:
                break
            
            self.logger.info(f"Still waiting for loaders: {active_loaders}")
            time.sleep(1)

        # 2. Wait for a main container to APPEAR and have children (actual rendering)
        # We prioritize specific route-content wrappers to avoid false positives from global shell
        content_selectors = [
            (By.CLASS_NAME, "route-content-os"),
            (By.CLASS_NAME, "route-content"),
            (By.CLASS_NAME, "event-bus-monitor-container"),
            (By.CLASS_NAME, "monitor-layout-grid"),
            (By.CLASS_NAME, "page-container"),
            (By.TAG_NAME, "main"),
            (By.ID, "root")
        ]
        
        for by, selector in content_selectors:
            try:
                # Wait for element presence
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((by, selector)))
                container = self.driver.find_element(by, selector)
                
                # Check for children (actual content)
                # We check for presence of children that aren't script/style AND have height > 0
                # NEW: Filter out common shell elements if we are matching 'main' or 'root'
                children = container.find_elements(By.XPATH, "./*[not(self::script or self::style or contains(@class, 'page-context-panel'))]")
                
                # High-fidelity render check: at least one child must have height > some threshold (e.g. 5px)
                rendered_content = False
                for child in children:
                    if child.is_displayed() and child.size.get('height', 0) > 5:
                        rendered_content = True
                        break
                
                if rendered_content:
                    self.logger.info(f"Content container {selector} detected with rendered children.")
                    return True
                else:
                    self.logger.info(f"Container {selector} exists but children lack sufficient height. Continuing wait...")
            except:
                continue
        
        self.logger.warning("Timeout reached: No non-empty rendered content detected.")
        return False

    def skip_modals(self):
        """Detects and skips known overlay modals (Onboarding, Tutorials)."""
        modal_selectors = [
            (By.CLASS_NAME, "skip-button"),
            (By.CLASS_NAME, "onboarding-skip"),
            (By.XPATH, "//button[contains(text(), 'Skip')]")
        ]
        
        for by, selector in modal_selectors:
            try:
                # Short timeout for existence check
                elements = self.driver.find_elements(by, selector)
                for el in elements:
                    if el.is_displayed():
                        self.logger.info(f"Auto-skipping modal using {selector}")
                        el.click()
                        time.sleep(2) # Increased wait for animation and re-render
                        return True
            except:
                continue
        return False

    def log_result(self, route: str, status: str, errors: List[str], screenshot_path: str, metadata: Optional[Dict] = None):
        """Appends result to daily JSON file. Deduplicates by route, keeping only the latest."""
        results_file = self.results_dir / self.results_filename
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "route": route,
            "status": status,
            "console_errors": errors,
            "screenshot": str(Path(screenshot_path).relative_to(PROJECT_ROOT)) if screenshot_path else None,
            "metadata": metadata or {}
        }
        
        data = []
        if results_file.exists():
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                pass
        
        # Deduplication: Remove existing entries for this route
        data = [d for d in data if d.get("route") != route]
        data.append(entry)
        
        # Sort data: Status != "SUCCESS" items first
        data.sort(key=lambda x: 0 if x.get("status") != "SUCCESS" else 1)
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to write results to {results_file}: {e}")

    def robust_login(self, base_url: str, email: str, password: str):
        """Performs a robust login flow with explicit waits."""
        self.logger.info(f"Attempting login for {email}...")
        self.driver.get(base_url)
        
        # Wait for either the dashboard marker or the login modal
        try:
            # Check if already logged in (look for MenuBar) - Fast check
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "menu-bar-container")))
            self.logger.info("Already logged in (MenuBar detected).")
            return True
        except TimeoutException:
            self.logger.info("Not logged in (or MenuBar not found yet). Proceeding to login...")
            pass

        try:
            # Fill email
            self.logger.info("Filling email...")
            email_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "email")))
            email_input.clear()
            email_input.send_keys(email)
            
            # Fill password
            self.logger.info("Filling password...")
            pass_input = self.driver.find_element(By.NAME, "password")
            pass_input.clear()
            pass_input.send_keys(password)
            
            # Click submit
            self.logger.info("Clicking submit...")
            submit_btn = self.driver.find_element(By.CLASS_NAME, "auth-button")
            submit_btn.click()
            self.logger.info("Submit clicked. Waiting for dashboard...")
            
            # 1. Look for primary dashboard markers (MenuBar or Orchestrator Logo)
            success_selectors = [
                (By.CLASS_NAME, "menu-bar-container"),
                (By.CLASS_NAME, "header-title"), 
                (By.XPATH, "//*[contains(text(), 'THE ORCHESTRATOR')]")
            ]
            
            for by, selector in success_selectors:
                try:
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((by, selector)))
                    self.logger.info(f"Login success detected via {selector}")
                    # Try to clear modals immediately after success detection
                    self.skip_modals()
                    return True
                except:
                    continue

            self.logger.error("Login verification timed out (No dashboard marker found).")
            self.capture_status("LOGIN_TIMEOUT", "root", errors=["Timed out waiting for dashboard markers."])
            return False
        except Exception as e:
            self.logger.error(f"Login flow error: {e}")
            self.capture_status("LOGIN_FAILED", "root", errors=[str(e)])
            return False

    def verify_route(self, url: str) -> Dict[str, Any]:
        """Verifies a single route, captures errors and screenshots."""
        self.driver.get(url)
        
        # NEW: Stricter robust wait (reduced timeout for speed)
        content_loaded = self.wait_for_page_ready(timeout=5)
        
        # Additional buffer for D3/Three.js or heavy animations
        if content_loaded:
            self.logger.info("Waiting 3s for full rendering safety buffer...")
            time.sleep(3)
        else:
            self.logger.info("Content empty/timeout. Skipping safety buffer.")
        
        route_path = url.split("127.0.0.1:5173")[-1]
        
        # Check for console errors
        logs = self.get_browser_logs()
        errors = [l['message'] for l in logs if l['level'] in ('SEVERE', 'ERROR')]
        
        # Check for UI error markers
        error_selectors = [
            ".error-boundary",
            ".crash-overlay",
            "#error-page",
            ".page-not-found"
        ]
        ui_failure = False
        for selector in error_selectors:
            try:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    ui_failure = True
                    self.logger.warning(f"UI Failure detected via selector: {selector}")
                    break
            except:
                continue

        # NEW: Stricter Black Screen / Empty Content Detection
        content_empty = False
        try:
            # Check for high-level container emptiness
            # We look specifically at route-content-os or route-content
            main_content = None
            for sel in [".route-content-os", ".route-content", "main"]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if el.is_displayed():
                        main_content = el
                        break
                except:
                    continue
            
            if main_content and not ui_failure:
                # Exclude shell components
                children = main_content.find_elements(By.XPATH, "./*[not(self::script or self::style or contains(@class, 'page-context-panel'))]")
                
                # Check for visible children with height
                has_meaningful_child = False
                for child in children:
                    if child.is_displayed() and child.size.get('height', 0) > 5:
                        has_meaningful_child = True
                        break
                
                if not has_meaningful_child:
                    # Also check if the text inside is just white space or shell text
                    text = main_content.text.strip()
                    if not text:
                        content_empty = True
            elif not ui_failure:
                # If no main content container found at all
                content_empty = True

            if content_empty:
                self.logger.warning(f"CONTENT_EMPTY detected for {url}!")
        except:
            pass

        # Targeted text check
        if not ui_failure:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.upper()
            critical_keywords = ["UNCAUGHT EXCEPTION", "RUNTIME ERROR", "REACT ERROR"]
            for kw in critical_keywords:
                if kw in body_text:
                    ui_failure = True
                    self.logger.warning(f"CRITICAL UI Failure detected via keyword: {kw}")
                    break

        # NOT_IMPLEMENTED Detection: Check for boilerplate/filler pages
        not_implemented = False
        if not content_empty and not ui_failure and not errors:
            try:
                # Check for SubPageBoilerplate component (CSS class)
                boilerplate_selectors = [
                    ".boilerplate-container",
                    ".boilerplate-content",
                ]
                for sel in boilerplate_selectors:
                    if self.driver.find_elements(By.CSS_SELECTOR, sel):
                        not_implemented = True
                        self.logger.warning(f"NOT_IMPLEMENTED: Boilerplate component detected via '{sel}'")
                        break

                # Check for workstation filler text patterns
                if not not_implemented:
                    body_text = self.driver.find_element(By.TAG_NAME, "body").text.upper()
                    filler_keywords = [
                        "SYNCING NEURAL MESH",
                        "SYNCHRONIZING MESH",
                        "ESTABLISHING HANDSHAKE WITH AGENTIC LAYER",
                        "INITIALIZING MESH",
                    ]
                    for kw in filler_keywords:
                        if kw in body_text:
                            not_implemented = True
                            self.logger.warning(f"NOT_IMPLEMENTED: Filler keyword '{kw}' detected")
                            break
            except Exception as e:
                self.logger.error(f"Error during NOT_IMPLEMENTED check: {e}")

        # Determine Status
        if errors or ui_failure:
            status = "FAILED"
        elif content_empty:
            status = "CONTENT_EMPTY"
        elif not_implemented:
            status = "NOT_IMPLEMENTED"
        else:
            status = "SUCCESS"
        
        screenshot = self.capture_status(
            status=status, 
            route=route_path, 
            errors=errors, 
            metadata={
                "ui_failure_detected": ui_failure,
                "content_loaded": content_loaded,
                "content_empty": content_empty,
                "not_implemented": not_implemented
            }
        )
        
        return {
            "status": status,
            "errors": errors,
            "screenshot": screenshot,
            "ui_failure_detected": ui_failure,
            "content_empty": content_empty,
            "not_implemented": not_implemented
        }
