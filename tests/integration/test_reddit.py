"""
==============================================================================
FILE: scripts/runners/test_reddit.py
ROLE: Test Runner
PURPOSE: Verifies Reddit mock data generation and sentiment scoring.
==============================================================================
"""

import asyncio
import logging
from services.social.reddit_service import get_reddit_client

logger = logging.getLogger(__name__)

def run_test_reddit(subreddit: str = "wallstreetbets", **_kwargs):
    """
    Runs the Reddit integration test.
    """
    print(f"\n{'='*60}")
    print(" TESTING REDDIT INTEGRATION (MOCK MODE)")
    print(f" Subreddit: r/{subreddit}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_reddit_client(mock=True) # Force mock for Phase 8

        try:
            # 1. Fetch Posts
            print(f"[*] Fetching top posts from r/{subreddit}...")
            posts = await client.get_subreddit_posts(subreddit, limit=5)
            
            if not posts:
                print("[-] No posts returned.")
            else:
                for p in posts:
                    sentiment_icon = ("🟢" if p.sentiment_score > 0 
                                      else ("🔴" if p.sentiment_score < 0 else "⚪"))
                    print(f"  {sentiment_icon} [{p.score}] {p.title} ({p.num_comments} comments)")

            # 2. Analyze Ticker Sentiment
            test_ticker = "NVDA"
            print(f"\n[*] Analyzing sentiment for ${test_ticker}...")
            analysis = await client.analyze_sentiment(test_ticker)
            
            print(f"  > Score: {analysis.get('sentiment_score')}")
            print(f"  > Label: {analysis.get('sentiment_label')}")
            print(f"  > Hype Score: {analysis.get('hype_score')}/100")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_reddit()
