import time
import requests
from datetime import datetime

ENDPOINTS = [
    ("Health", "http://127.0.0.1:5050/api/v1/health"),
    ("Departments", "http://127.0.0.1:5050/api/v1/departments"),
    ("Brokerage Positions", "http://127.0.0.1:5050/api/v1/brokerage/positions"),
    ("Homeostasis Status", "http://127.0.0.1:5050/api/v1/homeostasis/status"),
    ("Politics", "http://127.0.0.1:5050/api/v1/politics/disclosures")
]

def run_benchmarks():
    print(f"--- Benchmarking Started at {datetime.now()} ---")
    for name, url in ENDPOINTS:
        print(f"Testing {name} ({url})...")
        start = time.time()
        try:
            r = requests.get(url, timeout=35)
            elapsed = time.time() - start
            print(f"  Result: {r.status_code} in {elapsed:.4f}s")
        except Exception as e:
            elapsed = time.time() - start
            print(f"  FAILED {name} after {elapsed:.4f}s: {e}")
    print("--- Benchmarking Finished ---")

if __name__ == "__main__":
    run_benchmarks()
