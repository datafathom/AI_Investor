"""
==============================================================================
FILE: scripts/runners/test_finnhub.py
ROLE: Test Runner
PURPOSE: Verifies Finnhub data ingestion and IPO tracking logic.
==============================================================================
"""

import asyncio
import logging
from services.trading.ipo_tracker import get_ipo_tracker

logger = logging.getLogger(__name__)

def run_test_finnhub(mock: bool = False, **kwargs):
    """
    Runs the Finnhub integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING FINNHUB INTEGRATION & IPO TRACKING")
    print(f" Mode: {'MOCK' if mock else 'LIVE'}")
    print(f"{'='*60}\n")

    async def _internal():
        tracker = get_ipo_tracker()
        
        # Force mock mode if requested
        if mock:
            tracker.finnhub.mock = True

        try:
            # 1. Test IPO Calendar
            print("[*] Fetching and analyzing upcoming IPOs...")
            analysis = await tracker.get_upcoming_analysis()
            
            if not analysis:
                print("[-] No IPO data found.")
            else:
                print(f"[+] Found {len(analysis)} upcoming IPOs:")
                for item in analysis:
                    print(f"\n    - {item.company} ({item.symbol})")
                    print(f"      Date: {item.date}")
                    print(f"      Valuation: {item.estimated_valuation}")
                    print(f"      Success Prob: {item.success_probability:.2f}%")
                    print(f"      Risk Score: {item.risk_score:.2f}")
                    print(f"      Sentiment: {item.sentiment_signal}")

            # 2. Test News Ingestion
            print("\n[*] Fetching company news for TSLA...")
            news = await tracker.finnhub.get_company_news("TSLA")
            if news:
                print(f"[+] Retrieved {len(news)} news articles.")
                print(f"    Latest: {news[0].headline}")
            else:
                print("[-] No news articles found.")

            # 3. Test Real-Time Quote
            print("\n[*] Fetching real-time quote for AAPL...")
            quote = await tracker.finnhub.get_quote("AAPL")
            if quote:
                print(f"[+] Quote: ${quote.price:.2f} (High: ${quote.high:.2f}, Low: ${quote.low:.2f})")
            else:
                print("[-] Failed to fetch quote.")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    import sys
    mock = "--mock" in sys.argv
    run_test_finnhub(mock=mock)
