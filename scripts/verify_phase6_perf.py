import requests
import time
import concurrent.futures
import json

base_url = "http://127.0.0.1:5050/api/v1"

def test_cache():
    print("\n--- Testing Agent Cache ---")
    payload = {"agent_id": "synthesizer", "payload": {"action": "Market Summary", "data": {"ticker": "AAPL"}}}
    
    # First call (should be miss/real result)
    start = time.time()
    resp1 = requests.post(f"{base_url}/ai/agents/invoke", json=payload)
    elapsed1 = time.time() - start
    print(f"Call 1 (Potential MISS): {resp1.status_code}, time: {elapsed1:.2f}s")
    
    # Second call (should be hit/fast)
    start = time.time()
    resp2 = requests.post(f"{base_url}/ai/agents/invoke", json=payload)
    elapsed2 = time.time() - start
    print(f"Call 2 (Potential HIT): {resp2.status_code}, time: {elapsed2:.2f}s")
    
    if elapsed2 < elapsed1:
        print("✅ Cache working: Second call was faster.")
    else:
        print("⚠️ Cache check: Second call was not significantly faster (check backend logs).")

def invoke_worker(i):
    payload = {"agent_id": "synthesizer", "payload": {"action": f"Stress Test {i}", "data": {}}}
    requests.post(f"{base_url}/ai/agents/invoke", json=payload)

def test_concurrency():
    print("\n--- Testing Concurrency Limit (10) ---")
    print("Launching 15 simultaneous requests...")
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(invoke_worker, range(15))
    elapsed = time.time() - start
    print(f"Total time for 15 requests: {elapsed:.2f}s")
    print("Check backend logs to verify semaphore behavior (should see batches of 10).")

if __name__ == "__main__":
    try:
        test_cache()
        test_concurrency()
    except Exception as e:
        print(f"Verification failed: {e}")
