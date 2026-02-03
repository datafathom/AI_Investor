"""
==============================================================================
FILE: scripts/runners/test_youtube.py
ROLE: Test Runner
PURPOSE: Verifies YouTube Client and Transcript Analyzer in mock mode.
==============================================================================
"""

import asyncio
import logging
from services.social.youtube_client import get_youtube_client
from services.analysis.youtube_transcript_analyzer import get_youtube_analyzer

logger = logging.getLogger(__name__)

def run_test_youtube(mock: bool = True, **kwargs):
    """
    Runs the YouTube integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING YOUTUBE INTEGRATION (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_youtube_client(mock=True)
        analyzer = get_youtube_analyzer()

        try:
            # 1. Search Videos
            query = "Macro Liquidity"
            print(f"[*] Searching for '{query}' strategy videos...")
            videos = await client.search_videos(query)
            for v in videos[:2]:
                print(f"   🎥 [{v['channel']}] {v['title']}")

            # 2. Get Transcript
            target_id = videos[0]['video_id']
            print(f"\n[*] Fetching Transcript for {target_id}...")
            transcript = await client.get_video_transcript(target_id)
            print(f"   Transcript Snippet: {transcript[:80]}...")

            # 3. Analyze Video
            print(f"\n[*] Running AI Transcript Summarization...")
            analysis = await analyzer.analyze_video(target_id)
            print(f"   Sentiment: {analysis['sentiment_label']} ({analysis['sentiment_score']})")
            print(f"   Summary: {analysis['summary']}")
            print(f"   Symbols Detected: {analysis['extracted_tickers']}")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_youtube()
