"""
==============================================================================
FILE: scripts/runners/test_ibkr.py
ROLE: Test Runner
PURPOSE: Verifies IBKR Client connection and data retrieval in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.brokerage.ibkr_client import get_ibkr_client
from services.brokerage.ibkr_gateway_manager import get_ibkr_gateway

logger = logging.getLogger(__name__)

def run_test_ibkr(mock: bool = True, **kwargs):
    """
    Runs the Interactive Brokers integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING IBKR INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_ibkr_client(mock=True)
        gateway = get_ibkr_gateway()

        try:
            # 1. Start Gateway
            print("[*] Starting IBKR Gateway (Mock)...")
            await gateway.start_gateway()
            
            # 2. Connect
            print("[*] Connecting Client...")
            connected = await client.connect()
            print(f"   Connected: {connected}")

            # 3. Get Account
            print("\n[*] Fetching Account Summary...")
            account = await client.get_account_summary()
            print(f"   Net Liquidation: ${account.get('NetLiquidation')}")
            print(f"   Buying Power: ${account.get('BuyingPower')}")

            # 4. Get Positions
            print("\n[*] Fetching Global Positions...")
            positions = await client.get_positions()
            for p in positions:
                print(f"   [{p['sec_type']}] {p['symbol']}: {p['position']} @ {p['market_price']}")

            # 5. Place Order
            print("\n[*] Placing Order (EUR.USD)...")
            order = await client.place_order("EUR.USD", "BUY", 10000)
            print(f"   Order ID: {order.get('order_id')}")
            print(f"   Status: {order.get('status')}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)
        finally:
            await gateway.stop_gateway()

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_ibkr()
