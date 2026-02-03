
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from services.system.social_auth_service import get_social_auth_service

def verify_registration_flow():
    service = get_social_auth_service()
    
    print("\n--- Resetting Database ---")
    service.reset_database()
    print(f"User count: {len(service.users)}")
    assert len(service.users) == 0
    
    email = "astir@example.com"
    password = "supersecretpassword"
    
    print(f"\n--- Phase 1: Account Creation (Email/Password) ---")
    # Simulate register logic (from auth_api.py)
    service.users[email] = {
        "id": 1,
        "username": "astir",
        "role": "trader",
        "is_verified": False,
        "password_hash": f"mock_hash_{password[::-1]}",
        "linked_providers": {"email": {"registered_at": "2026-01-24"}}
    }
    print(f"User '{email}' created. ID: 1, Verified: False")
    assert service.users[email]['id'] == 1
    
    print("\n--- Phase 2: Login via Google (Merging) ---")
    # Use special 'email:' prefix mock logic to target the same email
    res_google = service.handle_callback("google", f"email:{email}")
    print(f"Google Login Success. User ID: {res_google['user']['id']}")
    print(f"Linked Providers: {list(service.users[email]['linked_providers'].keys())}")
    assert res_google['user']['id'] == 1
    assert "google" in service.users[email]['linked_providers']
    assert service.users[email]['is_verified'] == True # Trusted social provider verified the email
    
    print("\n--- Phase 3: Login via Venmo (Merging) ---")
    res_venmo = service.handle_callback("venmo", f"email:{email}")
    print(f"Venmo Login Success. User ID: {res_venmo['user']['id']}")
    print(f"Linked Providers: {list(service.users[email]['linked_providers'].keys())}")
    assert res_venmo['user']['id'] == 1
    assert "venmo" in service.users[email]['linked_providers']
    
    print("\n--- Phase 4: Confirm Identity Consistency ---")
    final_user = service.users[email]
    print(f"Final Identity: ID={final_user['id']}, Email={email}, Providers={list(final_user['linked_providers'].keys())}")
    assert final_user['id'] == 1
    assert len(final_user['linked_providers']) == 3 # email, google, venmo
    
    print("\n[SUCCESS] Fresh registration and multi-method merging flow verified!")

if __name__ == "__main__":
    try:
        verify_registration_flow()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[FAILURE] {e}")
        sys.exit(1)
