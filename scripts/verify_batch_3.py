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
            return True
        else:
            print(f"❌ Failure: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    # Login to get token
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

    # Batch 3 endpoints
    endpoints = [
        {"path": "/banking/accounts", "method": "GET"},
        {"path": "/billing/bill/upcoming/demo-user", "method": "GET"},
        {"path": "/budgeting/trends/demo-user", "method": "GET"},
        {"path": "/legal/documents", "method": "GET"},
        {"path": "/identity/profile", "method": "GET"},
        {"path": "/financial_planning/plan/demo-user", "method": "GET"},
        {"path": "/retirement/rmd/demo-user", "method": "GET"},
        {"path": "/tax_api/tax/harvesting/opportunities", "method": "GET"}
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
        print("\n🎉 All Batch 3 endpoints verified successfully!")
    else:
        print("\n⚠️ Some Batch 3 endpoints failed verification.")

if __name__ == "__main__":
    main()
