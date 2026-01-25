"""
==============================================================================
FILE: scripts/runners/test_research.py
ROLE: Test Runner
PURPOSE: Verifies ResearchAgent/PerplexityClient mock output.
==============================================================================
"""

import asyncio
import logging
from agents.research_agent import get_research_agent

logger = logging.getLogger(__name__)

def run_test_research(query: str = "Why is NVDA up today?", **_kwargs):
    """
    Runs the Research Agent test.
    """
    print(f"\n{'='*60}")
    print(" TESTING RESEARCH AGENT (MOCK MODE)")
    print(f" Query: {query}")
    print(f"{'='*60}\n")

    async def _internal():
        agent = get_research_agent(mock=True)

        try:
            print("[*] Thinking...")
            result = await agent.ask(query)
            
            print(f"\n🧠 ANSWER:")
            print(f"   {result['answer']}")
            print(f"\n📚 CITATIONS:")
            for idx, cit in enumerate(result['citations']):
                print(f"   [{idx+1}] {cit}")

            print("\n[!] VERIFICATION PASSED")

        except (ValueError, KeyError, RuntimeError) as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_research()
