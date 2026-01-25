
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from services.system.social_auth_service import get_social_auth_service

def test_account_merging():
    service = get_social_auth_service()
    
    # 1. Login via PayPal with 'merge' in code (assumes admin@example.com in mock)
    print("\n--- Phase 1: PayPal Login (Merge) ---")
    res1 = service.handle_callback("paypal", "merge_123")
    print(f"User ID: {res1['user']['id']}, Email: {res1['user']['email']}, New User: {res1['new_user']}")
    
    # 2. Login via Venmo with 'merge' in code
    print("\n--- Phase 2: Venmo Login (Merge) ---")
    res2 = service.handle_callback("venmo", "merge_456")
    print(f"User ID: {res2['user']['id']}, Email: {res2['user']['email']}, New User: {res2['new_user']}")
    
    # 3. Create a new user via Google
    print("\n--- Phase 3: Google Login (New) ---")
    res3 = service.handle_callback("google", "newuser_789")
    print(f"User ID: {res3['user']['id']}, Email: {res3['user']['email']}, New User: {res3['new_user']}")

    # 4. Verify same user ID for merged accounts
    assert res1['user']['id'] == res2['user']['id'] == 1
    assert res1['user']['email'] == res2['user']['email'] == "admin@example.com"
    assert res3['user']['id'] == 2
    assert res3['user']['email'] == "user_789@example.com"
    
    print("\n[SUCCESS] Account merging logic verified!")

if __name__ == "__main__":
    try:
        test_account_merging()
    except Exception as e:
        print(f"\n[FAILURE] {e}")
        sys.exit(1)
