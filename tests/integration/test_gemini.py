"""
==============================================================================
FILE: scripts/runners/test_gemini.py
ROLE: Test Runner
PURPOSE: Verifies Gemini/BriefingGenerator mock output.
==============================================================================
"""

import asyncio
import logging
from services.ai.briefing_generator import get_briefing_generator

logger = logging.getLogger(__name__)

def run_test_gemini(**_kwargs):
    """
    Runs the Gemini Briefing test.
    """
    print(f"\n{'='*60}")
    print(" TESTING GEMINI BRIEFING (MOCK MODE)")
    print(f"{'='*60}\n")

    async def _internal():
        generator = get_briefing_generator(mock=True)

        try:
            print("[*] Generating Daily Briefing...")
            briefing = await generator.get_daily_briefing()
            
            print(f"\n DATE: {briefing['date']}")
            print(f"SENTIMENT: {briefing['sentiment']}")
            
            print("\n🌍 MARKET OUTLOOK:")
            print(f"   {briefing['market_outlook']}")

            print("\n⏰ KEY EVENTS:")
            for event in briefing['key_events']:
                print(f"   - {event['time']}: {event['event']} ({event['impact']})")

            print("\n🔔 ALERTS:")
            for alert in briefing['portfolio_alerts']:
                print(f"   - [{alert['type'].upper()}] {alert['ticker']}: {alert['message']}")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_gemini()
