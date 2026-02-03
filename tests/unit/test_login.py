import requests
import time

def test_login(email, password):
    url = "http://localhost:5050/api/auth/login"
    payload = {"email": email, "password": password}
    try:
        response = requests.post(url, json=payload)
        print(f"Testing Login {email}: Status {response.status_code}")
        if response.status_code == 200:
            print(f"SUCCESS: {response.json().get('token')[:20]}...")
            return True
        else:
            print(f"FAILURE: {response.json()}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_register(email, password):
    url = "http://localhost:5050/api/auth/register"
    payload = {"email": email, "password": password}
    try:
        response = requests.post(url, json=payload)
        print(f"Testing Registration {email}: Status {response.status_code}")
        return response.status_code in [200, 201, 409]
    except Exception as e:
        print(f"ERROR: {e}")
        return False

# Wait for backend to start
time.sleep(1)

print("\n--- Testing Admin Login ---")
test_login("admin", "admin")

print("\n--- Testing Email Login ---")
test_login("admin@example.com", "admin")

test_email = f"test_{int(time.time())}@example.com"
print(f"\n--- Testing Flow for {test_email} ---")
if test_register(test_email, "password123"):
    test_login(test_email, "password123")
