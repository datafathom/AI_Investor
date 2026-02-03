
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from services.system.social_auth_service import get_social_auth_service

def test_advanced_auth():
    service = get_social_auth_service()
    email = "newuser@example.com"
    
    # Reset state for repeatable test
    if email in service.users:
        del service.users[email]

    print("\n--- Phase 1: Registration ---")
    # Simulate register logic (from auth_api.py)
    service.users[email] = {
        "id": 10,
        "username": "newuser",
        "role": "trader",
        "is_verified": False,
        "password_hash": "mock_initial_hash",
        "linked_providers": {"email": {"registered_at": "2026-01-24"}}
    }
    print(f"User created: {email}, Verified: {service.users[email]['is_verified']}")
    assert service.users[email]['is_verified'] == False
    
    print("\n--- Phase 2: Email Verification ---")
    success = service.verify_email(email)
    print(f"Verification Success: {success}, User Verified: {service.users[email]['is_verified']}")
    assert success == True
    assert service.users[email]['is_verified'] == True
    
    print("\n--- Phase 3: Social Login (Link to existing) ---")
    # Login via Google with the SAME email using special 'email:' prefix mock logic
    res = service.handle_callback("google", f"email:{email}") 
    print(f"Social ID: {res['user']['id']}, Providers: {list(service.users[email]['linked_providers'].keys())}")
    assert res['user']['id'] == 10
    assert "google" in service.users[email]['linked_providers']
    assert res['user']['has_password'] == True
    
    print("\n--- Phase 4: Add/Update Password ---")
    success = service.set_password(email, "mypassword123")
    print(f"Password Set: {success}, New Hash: {service.users[email]['password_hash']}")
    assert success == True
    assert "321drowssap" in service.users[email]['password_hash']
    
    print("\n[SUCCESS] Advanced auth features verified!")

if __name__ == "__main__":
    try:
        test_advanced_auth()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[FAILURE] {e}")
        sys.exit(1)
