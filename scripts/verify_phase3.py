import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5050/api/v1/admin"

def test_endpoint(method, path, data=None):
    url = f"{BASE_URL}{path}"
    print(f"Testing {method} {url}...")
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code < 400:
            print(f"✅ Success: {response.status_code}")
            return response.json()
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"💥 Exception: {e}")
        return None

def verify_phase3():
    print("=== Phase 3 API Verification ===")
    
    # 1. Ops API
    jobs = test_endpoint("GET", "/ops/jobs")
    if jobs:
        job_id = jobs[0]['id']
        test_endpoint("POST", f"/ops/jobs/{job_id}/trigger")
        test_endpoint("GET", f"/ops/jobs/{job_id}/runs")
    
    # 2. Workspaces API
    ws = test_endpoint("GET", "/workspaces")
    if ws:
        ws_id = ws[0]['id']
        test_endpoint("POST", f"/workspaces/{ws_id}/users", {"user_id": "tester", "role": "viewer"})
        test_endpoint("PATCH", f"/workspaces/{ws_id}/quotas", {"storage_gb": 20})
    
    # 3. Env API
    test_endpoint("GET", "/env")
    test_endpoint("GET", "/env/history")
    
    # 4. Features API
    flags = test_endpoint("GET", "/features")
    if flags:
        flag_name = list(flags.keys())[0]
        test_endpoint("POST", f"/features/{flag_name}/toggle")
        test_endpoint("POST", "/features/evaluate", {"name": flag_name, "context": {"user_id": "admin"}})

if __name__ == "__main__":
    verify_phase3()
