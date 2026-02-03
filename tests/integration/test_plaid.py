"""
==============================================================================
FILE: scripts/runners/test_plaid.py
ROLE: Test Runner
PURPOSE: Verifies PlaidClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.payments.plaid_service import get_plaid_client

logger = logging.getLogger(__name__)

def run_test_plaid(action: str = "flow", mock: bool = True, **kwargs):
    """
    Runs the Plaid integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING PLAID INTEGRATION (MOCK MODE)")
    print(f" Action: {action}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_plaid_client(mock=True)

        try:
            print(f"[*] Creating Link Token...")
            link_token_res = await client.create_link_token("user_test")
            print(f"   Token: {link_token_res['link_token']}")

            print(f"[*] Simulating Token Exchange...")
            # Simulate public token callback
            public_token = "public-sandbox-mock" 
            exchange_res = await client.exchange_public_token(public_token)
            access_token = exchange_res['access_token']
            print(f"   Access Token: {access_token}")

            print(f"[*] Fetching Accounts...")
            accounts = await client.get_accounts(access_token)
            for acc in accounts:
                 print(f"   - {acc['name']} ({acc['mask']}): ${acc['balances']['current']:.2f}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_plaid()
