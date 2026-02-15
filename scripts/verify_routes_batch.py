"""
===============================================================================
FILE: scripts/verify_routes_batch.py
ROLE: Batch Frontend Route Verifier
PURPOSE: Iterates through an array of URLs, applying robust verification
         and 8-attempt retry logic for failures.
===============================================================================
"""

import os
import sys
import time
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv

# Setup path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

from scripts.util.base_verifier import BaseVerifier

# URLs to test (can be passed via CLI or loaded from file)
DEFAULT_ROUTES = [
    "/",
    "/workspace/terminal",
    "/workspace/mission-control",
    "/analytics/strategy",
    "/settings"
]

def run_batch_verification(routes: list, max_retries: int = 8, dept_name: str = None):
    # Ensure int type for loop range
    max_retries = int(max_retries)
    verifier = BaseVerifier(headless=False, dept_name=dept_name)
    verifier.start_driver()
    
    # Get credentials from .env
    email = os.getenv("TEST_USER_EMAIL", "admin@aiinvestor.com")
    password = os.getenv("TEST_USER_PASSWORD", "password123")
    base_url = "http://localhost:5173"

    try:
        if not verifier.robust_login(base_url, email, password):
            verifier.logger.error("Initial login failed. Aborting batch.")
            return

        # Load existing results to skip ALREADY PROCESSED routes (Resume capability)
        existing_results = set()
        results_file = verifier.results_dir / verifier.results_filename
        if results_file.exists():
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Skip ANY route that has a status recorded for today
                    existing_results = {d.get("route") for d in data if d.get("status")}
                verifier.logger.info(f"Loaded {len(existing_results)} existing results to skip.")
            except Exception as e:
                verifier.logger.error(f"Failed to load existing results: {e}")

        for route in routes:
            if route in existing_results:
                verifier.logger.info(f"Skipping {route} - Already verified today.")
                continue

            full_url = f"{base_url}{route}"
            verifier.logger.info(f"--- Testing Route: {route} ---")
            
            success = False
            for attempt in range(1, max_retries + 1):
                verifier.logger.info(f"Attempt {attempt}/{max_retries} for {route}")
                result = verifier.verify_route(full_url)
                
                if result["status"] in ["SUCCESS", "NOT_IMPLEMENTED"]:
                    verifier.logger.info(f"[PASS] Route {route} finished with status {result['status']} on attempt {attempt}")
                    success = True
                    break
                else:
                    verifier.logger.warning(f"[FAIL] Route {route} failed with status {result['status']} on attempt {attempt}")
                    if result.get("errors"):
                        verifier.logger.warning(f"   Console Errors: {result['errors'][:2]}")
                    
                    # Wait a bit before retry
                    time.sleep(attempt * 2) 

            if not success:
                verifier.logger.error(f"[ERROR] Route {route} FAILED after {max_retries} attempts.")
                # We already logged the failure in JSON via verify_route

    finally:
        verifier.finalize_run()
        verifier.stop_driver()
        verifier.logger.info("Batch verification completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Frontend Route Verifier")
    parser.add_argument("--routes", nargs="+", help="Specific routes to test")
    parser.add_argument("--file", help="Path to file containing routes")
    parser.add_argument("--retries", type=int, default=8, help="Max retries per route")
    
    args = parser.parse_args()
    
    routes_to_test = DEFAULT_ROUTES
    if args.routes:
        routes_to_test = args.routes
    elif args.file:
        file_path = Path(args.file)
        if file_path.exists():
            with open(file_path, 'r') as f:
                routes_to_test = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            print(f"File not found: {args.file}")
            sys.exit(1)

    run_batch_verification(routes_to_test, args.retries)
