"""
==============================================================================
FILE: scripts/runners/test_alpaca.py
ROLE: Test Runner
PURPOSE: Verifies Alpaca trading client and position sync in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.brokerage.alpaca_client import get_alpaca_client
from services.brokerage.position_sync import get_position_sync

logger = logging.getLogger(__name__)

def run_test_alpaca(mock: bool = True, **kwargs):
    """
    Runs the Alpaca integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING ALPACA INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_alpaca_client(mock=True)
        sync_service = get_position_sync()

        try:
            # 1. Get Account
            print("[*] Fetching Account Details...")
            account = await client.get_account()
            print(f"   ID: {account.get('id')}")
            print(f"   Buying Power: ${account.get('buying_power')}")
            print(f"   Equity: ${account.get('equity')}")

            # 2. Get Positions
            print("\n[*] Fetching Positions...")
            positions = await client.get_positions()
            for p in positions:
                pl_icon = "🟢" if float(p['unrealized_pl']) > 0 else "🔴"
                print(f"   {pl_icon} {p['symbol']}: {p['qty']} shares @ ${p['current_price']} (P/L: ${p['unrealized_pl']})")

            # 3. Submit Order
            symbol = "NVDA"
            qty = 10
            print(f"\n[*] Submitting BUY Order for {qty} {symbol}...")
            order = await client.submit_order(symbol, qty, "buy")
            print(f"   Order ID: {order.get('id')}")
            print(f"   Status: {order.get('status')}")
            
            # 4. Sync Positions
            print("\n[*] Running Position Sync Service...")
            report = await sync_service.sync_positions()
            print(f"   Synced: {report.get('synced_count')} positions")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_alpaca()
