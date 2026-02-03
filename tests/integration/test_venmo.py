"""
==============================================================================
FILE: scripts/runners/test_venmo.py
ROLE: Test Runner
PURPOSE: Verifies VenmoClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.payments.venmo_service import get_venmo_client

logger = logging.getLogger(__name__)

def run_test_venmo(amount: float = 29.00, **_kwargs):
    """
    Runs the Venmo integration test.
    """
    print(f"\n{'='*60}")
    print(" TESTING VENMO INTEGRATION (MOCK MODE)")
    print(f" Amount: ${amount:.2f}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_venmo_client(mock=True)

        try:
            print("[*] Processing Payment...")
            txn = await client.process_payment(amount)
            print(f"   Transaction ID: {txn['id']}")
            print(f"   Status: {txn['status']}")
            print(f"   Payer: {txn['payer']['display_name']} ({txn['payer']['username']})")
            print(f"   Method: {txn['payment_method']}")
            print(f"   Note: {txn['note']}")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_venmo()
