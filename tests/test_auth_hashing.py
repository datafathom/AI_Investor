import unittest
import json
import requests
import time

class TestAuthHashing(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5050/api/auth"

    def setUp(self):
        self.timestamp = int(time.time())
        self.email = f"test_hash_{self.timestamp}@example.com"
        self.password = "ValidPass123!"

    def test_registration_versus_login_hashing(self):
        """Verify that a user registered with a password can log in with the same password."""
        # 1. Register
        reg_payload = {
            "email": self.email,
            "password": self.password
        }
        reg_res = requests.post(f"{self.BASE_URL}/register", json=reg_payload)
        self.assertEqual(reg_res.status_code, 200, f"Registration failed: {reg_res.text}")
        
        # 2. Verify Email (Mock)
        verify_res = requests.get(f"{self.BASE_URL}/verify-email?email={self.email}&token=mock_verify_token")
        self.assertEqual(verify_res.status_code, 200)

        # 3. Login with EXACT same email/password
        login_payload = {
            "email": self.email,
            "password": self.password
        }
        login_res = requests.post(f"{self.BASE_URL}/login", json=login_payload)
        self.assertEqual(login_res.status_code, 200, f"Login failed for {self.email} with 200 code: {login_res.text}")
        
        # 4. Login with case-insensitive email
        login_payload_upper = {
            "email": self.email.upper(),
            "password": self.password
        }
        login_res_upper = requests.post(f"{self.BASE_URL}/login", json=login_payload_upper)
        self.assertEqual(login_res_upper.status_code, 200, "Login failed with uppercase email")

    def test_invalid_credentials(self):
        """Verify that wrong password returns 401."""
        # Register a user
        email = f"wrong_pass_{self.timestamp}@example.com"
        requests.post(f"{self.BASE_URL}/register", json={"email": email, "password": "correct"})
        
        # Try wrong password
        login_res = requests.post(f"{self.BASE_URL}/login", json={"email": email, "password": "wrong"})
        self.assertEqual(login_res.status_code, 401)

if __name__ == "__main__":
    unittest.main()
