import requests
import json

url = "http://127.0.0.1:5050/api/v1/auth/login"
payload = {
    "email": "admin",
    "password": "makeMoney"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
