
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5050/api/v1/dev"

def test_status():
    print(f"Testing {BASE_URL}/status...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("âœ… Status Check Passed")
            return True
        else:
            print("â Œ Status Check Failed")
            return False
    except Exception as e:
        print(f"â Œ Status Check Exception: {e}")
        return False

def test_generate():
    print(f"\nTesting {BASE_URL}/generate...")
    payload = {
        "task": "Create a hello world python function",
        "context": {}
    }
    try:
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {response.text}") # Verbose
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "code" in data:
                print("âœ… Generate Check Passed")
                return True
        print("â Œ Generate Check Failed")
        return False
    except Exception as e:
        print(f"â Œ Generate Check Exception: {e}")
        return False

def test_deploy_mismatch():
    print(f"\nTesting {BASE_URL}/deploy (Expect 404/405 if missing)...")
    payload = {
        "name": "test_agent",
        "code": "print('hello')"
    }
    try:
        response = requests.post(f"{BASE_URL}/deploy", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 404:
            print("âœ… Confirmed /deploy is MISSING (As expected due to mismatch)")
            return True # This confirms our findings
        elif response.status_code == 200:
            print("â Œ /deploy actually exists? (Unexpected)")
            return False
        else:
             print(f"âš ï¸  /deploy returned {response.status_code}")
             return True
    except Exception as e:
        print(f"â Œ Deploy Check Exception: {e}")
        return False

if __name__ == "__main__":
    s1 = test_status()
    s2 = test_generate()
    s3 = test_deploy_mismatch()
    
    if s1 and s2 and s3:
        print("\nAll checks completed as analyzed.")
        sys.exit(0)
    else:
        print("\nSome checks failed.")
        sys.exit(1)
