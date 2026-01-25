"""
==============================================================================
FILE: scripts/runners/test_debate.py
ROLE: Test Runner
PURPOSE: Verifies DebateChamberAgent flow and mock personas.
==============================================================================
"""

import asyncio
import logging
from agents.debate_chamber_agent import get_debate_agent

logger = logging.getLogger(__name__)

def run_test_debate(ticker: str = "SPY", **_kwargs):
    """
    Runs the Debate Chamber test.
    """
    print(f"\n{'='*60}")
    print(" TESTING DEBATE CHAMBER (MOCK MODE)")
    print(f" Subject: {ticker}")
    print(f"{'='*60}\n")

    async def _internal():
        agent = get_debate_agent(mock=True)

        try:
            print(f"[*] Convening Debate Chamber for {ticker}...")
            print("    > Persons Analyzing: BULL, BEAR, MODERATOR")
            
            result = await agent.conduct_debate(ticker)
            
            print(f"\n[+] 🐂 BULL THESIS:")
            print(f"    {result['bull_thesis']}")

            print(f"\n[+] 🐻 BEAR THESIS:")
            print(f"    {result['bear_thesis']}")

            print(f"\n[+]  CONSENSUS:")
            print(f"    {result['consensus']}")

            print(f"\n[*] FINAL VERDICT: {result['verdict']} (Score: {result['score']}/100)")
            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_debate()
