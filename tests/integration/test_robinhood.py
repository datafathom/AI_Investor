"""
==============================================================================
FILE: scripts/runners/test_robinhood.py
ROLE: Test Runner
PURPOSE: Verifies Robinhood Mock Client authentication and portfolio retrieval.
==============================================================================
"""

import asyncio
import logging
from services.brokerage.robinhood_client import get_robinhood_client

logger = logging.getLogger(__name__)

def run_test_robinhood(mock: bool = True, **kwargs):
    """
    Runs the Robinhood integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING ROBINHOOD INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_robinhood_client(mock=True)

        try:
            # 1. Login
            print("[*] Authenticating User...")
            success = await client.login("demo_user", "password123")
            print(f"   Success: {success}")
            
            if success:
                # 2. Get Profile
                print("\n[*] Fetching User Profile...")
                profile = await client.get_user_profile()
                print(f"   Msg: Welcome, {profile.get('username')}")
                print(f"   Buying Power: ${profile.get('cash_available')}")

                # 3. Get Holdings
                print("\n[*] Fetching Portfolio Holdings...")
                holdings = await client.get_holdings()
                for h in holdings:
                    icon = "🪙" if h['type'] == 'crypto' else "📈"
                    print(f"   {icon} {h['symbol']}: {h['quantity']} @ ${h['current_price']} (Equity: ${h['equity']})")

                print(f"\n[!] VERIFICATION PASSED")
            else:
                print("[-] Login failed.")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_robinhood()
