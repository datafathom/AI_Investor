"""
==============================================================================
FILE: scripts/runners/test_stocktwits.py
ROLE: Test Runner
PURPOSE: Verifies StockTwits Client and Sentiment Analyzer in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.social.stocktwits_client import get_stocktwits_client
from services.analysis.stocktwits_sentiment import get_stocktwits_sentiment

logger = logging.getLogger(__name__)

def run_test_stocktwits(mock: bool = True, **kwargs):
    """
    Runs the StockTwits integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING STOCKTWITS INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_stocktwits_client(mock=True)
        analyzer = get_stocktwits_sentiment()

        try:
            # 1. Trending Symbols
            print("[*] Fetching Trending Tickers...")
            trending = await client.get_trending_symbols()
            for t in trending:
                print(f"   🔥 {t['symbol']} ({t['name']}) - Score: {t['trending_score']}")

            # 2. Symbol Stream
            target = "BTC.X"
            print(f"\n[*] Fetching Real-time Stream for {target}...")
            stream = await client.get_symbol_stream(target)
            for m in stream[:3]: # Show first 3
                sent = m.get('entities', {}).get('sentiment', {}).get('basic') if m.get('entities') else "Neutral"
                print(f"   [{sent}] @{m['user']['username']}: {m['body'][:40]}...")

            # 3. Sentiment Analysis
            print(f"\n[*] Calculating Sentiment Consensus for {target}...")
            analysis = await analyzer.analyze_symbol(target)
            print(f"   Consensus: {analysis['consensus']}")
            print(f"   Bullish Count: {analysis['bull_count']}")
            print(f"   Bearish Count: {analysis['bear_count']}")
            print(f"   Sentiment Score: {analysis['sentiment_score']}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_stocktwits()
