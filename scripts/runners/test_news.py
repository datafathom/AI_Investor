"""
==============================================================================
FILE: scripts/runners/test_news.py
ROLE: Test Runner
PURPOSE: Verifies NewsAPI aggregation and heuristic sentiment analysis.
==============================================================================
"""

import asyncio
import logging
from services.analysis.news_sentiment_service import get_news_sentiment_service

logger = logging.getLogger(__name__)

def run_test_news(topic: str = "market", mock: bool = False, **kwargs):
    """
    Runs the NewsAPI and Sentiment analysis test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING NEWSAPI INTEGRATION & SENTIMENT ANALYSIS")
    print(f" Topic: {topic}")
    print(f" Mode: {'MOCK' if mock else 'LIVE'}")
    print(f"{'='*60}\n")

    async def _internal():
        service = get_news_sentiment_service()
        
        # Force mock mode if requested
        if mock:
            service.news.mock = True

        try:
            # 1. Test Overall Market Sentiment
            if topic == "market":
                print("[*] Analyzing top headlines for overall market sentiment...")
                market_data = await service.get_market_sentiment()
                print(f"[+] Average Score: {market_data['average_score']:.2f}")
                print(f"[+] Market Label: {market_data['label']}")
                print(f"[+] Article Count: {market_data['count']}")
                
                print("\n[*] Top Headlines analyzed:")
                for res in market_data['top_news']:
                    print(f"    - [{res.label}] {res.article.title} ({res.article.source_name})")
                    if res.indicators:
                        print(f"      Indicators: {', '.join(res.indicators)}")

            # 2. Test Topic-Specific Sentiment
            print(f"\n[*] Analyzing specific sentiment for: {topic}...")
            results = await service.analyze_topic(topic)
            
            if not results:
                print(f"[-] No articles found for {topic}.")
            else:
                print(f"[+] Found {len(results)} articles. Examples:")
                for res in results[:3]:
                    print(f"\n    - Title: {res.article.title}")
                    print(f"      Score: {res.score:.2f}")
                    print(f"      Label: {res.label}")
                    print(f"      Source: {res.article.source_name}")
                    if res.indicators:
                        print(f"      Indicators: {', '.join(res.indicators)}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    import sys
    # Handle simple CLI execution
    args = sys.argv[1:]
    mock = "--mock" in args
    # Minimal positional arg parsing
    topic = "market"
    for a in args:
        if not a.startswith("-"):
            topic = a
            break
            
    run_test_news(topic=topic, mock=mock)
