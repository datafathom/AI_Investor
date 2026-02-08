import requests
import json
import sys
import time

BASE_URL = "http://localhost:5050/api/v1"

def test_endpoint(method, path, data=None):
    url = f"{BASE_URL}{path}"
    print(f"[{method}] Requesting: {url}")
    try:
        startTime = time.time()
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        duration = (time.time() - startTime) * 1000
        
        if response.status_code == 200:
            print(f"  [PASS] Status: 200 (Time: {duration:.1f}ms)")
            return True
        else:
            print(f"  [FAIL] Status: {response.status_code}")
            print(f"  [BODY] {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    finally:
        time.sleep(0.5)

def run_tests():
    print("--- Phase 4 API Diagnostic ---")
    results = []
    
    # 1. Forced Sellers (Base prefix /market-data)
    results.append(test_endpoint("GET", "/market-data/forced-sellers/fragility/AAPL"))
    results.append(test_endpoint("GET", "/market-data/forced-sellers/heatmap"))
    results.append(test_endpoint("GET", "/market-data/forced-sellers/liquidity-traps"))
    
    # 2. Whale Flow (Base prefix /market-data)
    results.append(test_endpoint("GET", "/market-data/whale-flow"))
    results.append(test_endpoint("GET", "/market-data/whale-flow/filings?limit=5"))
    results.append(test_endpoint("GET", "/market-data/whale-flow/crowding"))
    
    # 3. Promotions (Base prefix /market-data)
    results.append(test_endpoint("GET", "/market-data/promotions"))
    
    # 4. Indicators (Base prefix /indicators)
    results.append(test_endpoint("GET", "/indicators"))
    results.append(test_endpoint("POST", "/indicators/calculate", {
        "ticker": "AAPL",
        "indicator": "rsi",
        "period": "1y",
        "params": {"period": 14}
    }))
    
    # 5. Market Regime (Base prefix /market)
    results.append(test_endpoint("GET", "/market/regime"))
    
    print("\n--- Diagnostic Summary ---")
    success_count = results.count(True)
    total_count = len(results)
    print(f"Passed: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("RESULT: ALL_SYSTEMS_OPERATIONAL")
        sys.exit(0)
    else:
        print("RESULT: DEGRADED_STATE")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
