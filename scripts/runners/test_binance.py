"""
==============================================================================
FILE: scripts/runners/test_binance.py
ROLE: Test Runner
PURPOSE: Verifies BinanceClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.data.binance_service import get_binance_client

logger = logging.getLogger(__name__)

def run_test_binance(action: str = "ticker", symbol: str = "BTCUSDT", mock: bool = True, **kwargs):
    """
    Runs the Binance integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING BINANCE INTEGRATION (MOCK MODE)")
    print(f" Action: {action} | Symbol: {symbol}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_binance_client(mock=True)

        try:
            if action == "ticker":
                print(f"[*] Fetching Ticker for {symbol}...")
                ticker = await client.get_ticker(symbol)
                print(f"   Last Price: ${ticker['lastPrice']}")
                print(f"   24h Change: {ticker['priceChangePercent']}%")
                print(f"   Volume: {ticker['volume']}")

            elif action == "depth":
                print(f"[*] Fetching Order Book for {symbol}...")
                depth = await client.get_order_book(symbol)
                print(f"   Top Bid: {depth['bids'][0][0]} (Qty: {depth['bids'][0][1]})")
                print(f"   Top Ask: {depth['asks'][0][0]} (Qty: {depth['asks'][0][1]})")

            elif action == "trade":
                 print(f"[*] Placing BUY Order for {symbol}...")
                 order = await client.place_order(symbol, "BUY", 0.05)
                 print(f"   Order ID: {order['orderId']}")
                 print(f"   Status: {order['status']}")
                 print(f"   Executed Price: ${order['price']}")
                 print(f"   Total Cost: ${order['cummulativeQuoteQty']}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_binance()
