
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from services.system.social_auth_service import get_social_auth_service

def test_fund_transfers():
    service = get_social_auth_service()
    email = "banker@example.com"
    
    print("\n--- Phase 1: Social Login with Plaid ---")
    # Simulate first-time login via Plaid
    res = service.handle_callback("plaid", f"email:{email}")
    print(f"User created: {email}, ID: {res['user']['id']}")
    assert res['user']['email'] == email
    
    print("\n--- Phase 2: Check Linked Finance Vendors ---")
    vendors = service.get_linked_finance_vendors(email)
    print(f"Linked Vendors: {vendors}")
    assert "plaid" in vendors
    
    print("\n--- Phase 3: Initiate Fund Transfer ---")
    transfer_res = service.transfer_funds(email, "plaid", 500.0, "deposit")
    print(f"Transfer Result: {transfer_res}")
    assert transfer_res["success"] == True
    assert transfer_res["amount"] == 500.0
    
    print("\n--- Phase 4: Social Login with Venmo (Merging) ---")
    # Simulate login via Venmo with same email
    res2 = service.handle_callback("venmo", f"email:{email}")
    print(f"Merged login success. ID: {res2['user']['id']}")
    assert res2['user']['id'] == res['user']['id']
    
    vendors_updated = service.get_linked_finance_vendors(email)
    print(f"Updated Linked Vendors: {vendors_updated}")
    assert "venmo" in vendors_updated
    assert "plaid" in vendors_updated
    
    print("\n[SUCCESS] Linked vendor fund transfers verified end-to-end!")

if __name__ == "__main__":
    try:
        test_fund_transfers()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[FAILURE] {e}")
        sys.exit(1)
