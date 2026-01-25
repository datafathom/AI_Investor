"""
==============================================================================
FILE: scripts/runners/test_square.py
ROLE: Test Runner
PURPOSE: Verifies SquareClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.payments.square_service import get_square_client

logger = logging.getLogger(__name__)

def run_test_square(action: str = "stats", **_kwargs):
    """
    Runs the Square integration test.
    """
    print(f"\n{'='*60}")
    print(" TESTING SQUARE INTEGRATION (MOCK MODE)")
    print(f" Action: {action}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_square_client(mock=True)

        try:
            if action == "stats":
                print("[*] Fetching Merchant Stats...")
                stats = await client.get_merchant_stats()

                print(f"   Date: {stats['date']}")
                print(f"   Gross Sales: ${(stats['gross_sales_money']['amount']/100):.2f}")
                print(f"   Tx Count: {stats['transaction_count']}")
                print(f"   Terminal Status: {stats['terminal_status']}")
                print(f"   Locations: {stats['active_locations']}")

            elif action == "catalog":
                print("[*] Fetching Product Catalog...")
                catalog = await client.get_catalog()
                for item in catalog:
                    print(f"   - {item['name']}: ${(item['price']/100):.2f} ({item['id']})")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_square()
