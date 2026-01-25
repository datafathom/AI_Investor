"""
==============================================================================
FILE: scripts/runners/test_coinbase.py
ROLE: Test Runner
PURPOSE: Verifies Coinbase Client and Custody service in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.crypto.coinbase_client import get_coinbase_client
from services.crypto.coinbase_custody import get_coinbase_custody

logger = logging.getLogger(__name__)

def run_test_coinbase(mock: bool = True, **kwargs):
    """
    Runs the Coinbase integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING COINBASE CLOUD INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_coinbase_client(mock=True)
        custody = get_coinbase_custody(mock=True)

        try:
            # 1. Fetch Accounts
            print("[*] Fetching Trading Accounts...")
            accounts = await client.get_accounts()
            for acc in accounts:
                print(f"   {acc['currency']}: {acc['balance']} (Avail: {acc['available']})")

            # 2. Get Product Price
            print("\n[*] Fetching BTC-USD Institutional Quote...")
            product = await client.get_product("BTC-USD")
            print(f"   Price: ${product['price']} {product['quote_currency']}")

            # 3. Place Order
            print("\n[*] Placing Institutional BUY Order...")
            order = await client.place_order("BTC-USD", "BUY", {"count": "0.1"})
            print(f"   Order ID: {order['order_id']}")
            print(f"   Status: {order['status']}")

            # 4. Custody Check
            print("\n[*] Auditing Cold Storage Vaults...")
            vaults = await custody.get_vault_balances()
            for v in vaults:
                print(f"   [{v['status']}] {v['vault_name']}: {v['total_amount']} {v['asset']} (Approvals: {v['approvals_required']})")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_coinbase()
