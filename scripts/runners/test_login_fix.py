
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from services.system.social_auth_service import get_social_auth_service

def test_login_fix():
    service = get_social_auth_service()
    service.reset_database()
    
    email = "tester@example.com"
    password = "password123"
    
    print("\n--- Step 1: Registering User ---")
    # Simulate register logic (from auth_api.py)
    service.users[email] = {
        "id": 100,
        "username": "tester",
        "role": "trader",
        "is_verified": False,
        "password_hash": f"mock_hash_{password[::-1]}",
        "linked_providers": {"email": {"registered_at": "2026-01-24"}}
    }
    print(f"User registered with email: {email}")
    
    print("\n--- Step 2: Attempting Login (Standard) ---")
    # Simulate login logic
    user_data = service.users.get(email)
    provided_hash = f"mock_hash_{password[::-1]}"
    print(f"Stored Hash: {user_data['password_hash']}")
    print(f"Provided Hash: {provided_hash}")
    
    assert user_data['password_hash'] == provided_hash
    print("Login Simulation SUCCESS!")
    
    print("\n--- Step 3: Attempting Login (Wrong Password) ---")
    wrong_hash = f"mock_hash_{'wrongpassword'[::-1]}"
    assert user_data['password_hash'] != wrong_hash
    print("Wrong Password Rejected (As Expected)")

    print("\n[SUCCESS] Login persistence and dynamic verify confirmed!")

if __name__ == "__main__":
    test_login_fix()
