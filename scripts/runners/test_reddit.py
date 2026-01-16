"""
==============================================================================
FILE: scripts/runners/test_reddit.py
ROLE: Sentiment Tester
PURPOSE: Verifies Reddit mention tracking and FinBERT sentiment.
USAGE: python cli.py test-reddit --tickers "TSLA,NVDA,BTC"
INPUT/OUTPUT:
    - Input: List of tickers
    - Output: Mention counts and sentiment polarity.
==============================================================================
"""

import logging
from services.data.reddit_service import RedditService

logger = logging.getLogger(__name__)

def run_test_reddit(tickers: str = "TSLA,NVDA,SPY", **kwargs):
    """
    Test runner for Reddit sentiment analysis.
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    print(f"--- Analyzing Reddit Sentiment for {ticker_list} ---")
    
    service = RedditService()
    results = service.track_mentions(ticker_list)
    
    print("\nResults:")
    print("-" * 30)
    for ticker, data in results.items():
        sentiment_label = "BULLISH" if data['sentiment'] > 0.1 else "BEARISH" if data['sentiment'] < -0.1 else "NEUTRAL"
        print(f"[{ticker}] Mentions: {data['mentions']} | Sentiment: {data['sentiment']:.2f} ({sentiment_label})")
    print("-" * 30)
    
    return True
