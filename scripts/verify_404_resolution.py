import requests
import json

endpoints = [
    "http://127.0.0.1:5050/api/v1/brokerage/status",
    "http://127.0.0.1:5050/api/v1/brokerage/providers",
    "http://127.0.0.1:5050/api/v1/brokerage/positions",
    "http://127.0.0.1:5050/api/v1/homeostasis/status"
]

for url in endpoints:
    try:
        response = requests.get(url, timeout=5)
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error for {url}: {e}")
