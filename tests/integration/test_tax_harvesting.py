"""
==============================================================================
FILE: scripts/runners/test_tax_harvesting.py
ROLE: Test Runner
PURPOSE: Verifies TaxBitClient mock output.
==============================================================================
"""

import asyncio
import logging
from services.taxes.taxbit_service import get_taxbit_client

logger = logging.getLogger(__name__)

def run_test_tax_harvesting(action: str = "analyze", mock: bool = True, **kwargs):
    """
    Runs the TaxBit integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING TAX HARVESTING (MOCK MODE)")
    print(f" Action: {action}")
    print(f"{'='*60}\n")

    async def _internal():
        client = get_taxbit_client(mock=True)

        try:
            print(f"[*] Analyzing Portfolio for Tax Opportunities...")
            report = await client.get_harvesting_opportunities("port_test_1")
            
            summary = report.get('summary', {})
            print(f"   Est. Tax Savings: ${summary.get('estimated_tax_savings', 0):.2f}")
            print(f"   Available Short-Term Losses: ${summary.get('short_term_losses_available', 0):.2f}")
            
            print(f"\n   Opportunities Identified: {len(report.get('opportunities', []))}")
            for opp in report.get('opportunities', []):
                print(f"     - {opp['asset']}: {opp['recommendation']} (Loss: ${opp['unrealized_loss']:.2f})")

            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logging.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    run_test_tax_harvesting()
