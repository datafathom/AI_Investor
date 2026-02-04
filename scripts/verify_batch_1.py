import requests
import json
import time

BASE_URL = "http://127.0.0.1:5050/api/v1"

def test_endpoint(endpoint, method="GET", data=None, headers=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {method} {url}...")
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        
        print(f"Status: {response.status_code}")
        if response.status_code < 400:
            print("✅ Success")
            # print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Failure: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    # Login to get token (using admin fallback)
    print("Logging in...")
    login_url = "http://127.0.0.1:5050/api/v1/auth/login"
    login_data = {"email": "admin", "password": "makeMoney"}
    resp = requests.post(login_url, json=login_data)
    if resp.status_code != 200:
        print("Failed to login")
        return
    
    token = resp.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Token acquired.")

    # Updated endpoints based on prefix alignment
    endpoints = [
        {"path": "/onboarding/status", "method": "GET"},
        {"path": "/analytics/performance-attribution", "method": "GET", "params": {"portfolio_id": "demo-portfolio"}},
        {"path": "/attribution/benchmarks", "method": "GET"},
        {"path": "/ai/briefing/daily", "method": "GET"},
        {"path": "/execution/trailing-stop", "method": "POST", "data": {
            "user_id": "0", "symbol": "AAPL", "quantity": 10, "trailing_value": 5.0
        }},
        {"path": "/ai_assistant/recommendations/0", "method": "GET"}
    ]

    results = []
    for ep in endpoints:
        results.append(test_endpoint(
            ep["path"], 
            ep["method"], 
            data=ep.get("data"), 
            headers=headers,
            params=ep.get("params")
        ))
    
    if all(results):
        print("\n🎉 All Batch 1 endpoints verified successfully!")
    else:
        print("\n⚠️ Some endpoints failed verification.")

if __name__ == "__main__":
    main()
