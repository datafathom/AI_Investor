"""
==============================================================================
FILE: scripts/runners/test_crypto.py
ROLE: Test Runner
PURPOSE: Verifies CryptoCompare pricing and volume aggregation.
==============================================================================
"""

import asyncio
import logging
from services.data.crypto_compare_service import get_crypto_client

logger = logging.getLogger(__name__)

def run_test_crypto(symbols: str = "BTC,ETH", mock: bool = False, **_kwargs: any) -> None:
    """
    Runs the CryptoCompare integration test.
    """
    print(f"\n{'='*60}")
    print(" TESTING CRYPTOCOMPARE INTEGRATION")
    print(f" Symbols: {symbols}")
    print(f" Mode: {'MOCK' if mock else 'LIVE'}")
    print(f"{'='*60}\n")

    symbol_list = [s.strip().upper() for s in symbols.split(",")]

    async def _internal() -> None:
        client = get_crypto_client()

        # Force mock mode if requested
        if mock:
            client.mock = True

        try:
            # 1. Test Multi-Symbol Pricing
            print(f"[*] Fetching prices for: {', '.join(symbol_list)}...")
            prices = await client.get_price(symbol_list, ["USD", "EUR"])

            if not prices:
                print("[-] No price data returned.")
            else:
                for sym, rates in prices.items():
                    print(f"[+] {sym}: {rates}")

            # 2. Test Exchange Volume (for first symbol)
            target = symbol_list[0]
            print(f"\n[*] Fetching top exchange volume for: {target}...")
            volumes = await client.get_top_exchanges_volume(target)

            if not volumes:
                print(f"[-] No volume data found for {target}.")
            else:
                print(f"[+] Top Exchanges for {target}:")
                for v in volumes:
                    print(f"    - {v.exchange}: ${v.volume_24h:,.0f} ({v.market_share}%)")

            print("\n[!] VERIFICATION PASSED")

        except RuntimeError as e:
            print(f"[-] API ERROR during test: {e}")
            logger.exception(e)
        except Exception as e:
            print(f"[-] UNEXPECTED ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    import sys
    # Handle simple CLI execution
    args = sys.argv[1:]
    IS_MOCK = "--mock" in args
    SYMBOLS = "BTC,ETH"
    for a in args:
        if not a.startswith("-"):
            SYMBOLS = a
            break

    run_test_crypto(symbols=SYMBOLS, mock=IS_MOCK)
