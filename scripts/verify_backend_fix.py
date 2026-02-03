import requests
import json

def verify_homeostasis():
    url = "http://127.0.0.1:5050/api/v1/homeostasis/status"
    # Note: This might require auth depending on how strict the mock is, 
    # but we can at least check if it's a 500 or something else.
    try:
        # We try to get the status. If it's 401/302, it means the route exists but needs login.
        # If it's 500, it's still broken.
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: Homeostasis API is up and responding!")
            print(json.dumps(response.json(), indent=2))
        elif response.status_code in [401, 302]:
            print("INFO: Route exists but requires authentication (expected).")
        else:
            print(f"FAILURE: Received status {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_homeostasis()
