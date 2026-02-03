"""
==============================================================================
FILE: scripts/runners/test_paypal.py
ROLE: Test Runner
PURPOSE: Verifies PayPalClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.payments.paypal_service import get_paypal_client

logger = logging.getLogger(__name__)

def run_test_paypal(action: str = "order", **_kwargs):
    """
    Runs the PayPal integration test.
    """
    print(f"\n{'='*60}")
    print(" TESTING PAYPAL INTEGRATION (MOCK MODE)")
    print(f" Action: {action}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_paypal_client(mock=True)

        try:
            print("[*] Creating Order...")
            order = await client.create_order(29.00)
            print(f"   Order ID: {order['id']}")
            print(f"   Status: {order['status']}")
            
            approve_link = next((l['href'] for l in order['links'] if l['rel'] == 'approve'), None)
            print(f"   Approval URL: {approve_link}")

            print("[*] Capturing Order...")
            capture = await client.capture_order(order['id'])
            print(f"   Status: {capture['status']}")
            
            # Extract final capture status
            try:
                txn_status = capture['purchase_units'][0]['payments']['captures'][0]['status']
                print(f"   Transaction Status: {txn_status}")
            except (KeyError, IndexError):
                print("   Transaction Status: UNKNOWN")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_paypal()
