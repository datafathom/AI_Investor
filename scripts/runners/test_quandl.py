"""
==============================================================================
FILE: scripts/runners/test_quandl.py
ROLE: Test Runner
PURPOSE: Verifies Quandl data ingestion and Short Interest analysis logic.
==============================================================================
"""

import asyncio
import logging
import json
from services.analysis.short_interest_service import get_short_interest_service

logger = logging.getLogger(__name__)

def run_test_quandl(symbol: str = "TSLA", mock: bool = False, **kwargs):
    """
    Runs the Quandl integration test.
    """
    print(f"\n{'='*60}")
    print(f" TESTING QUANDL INTEGRATION & ANALYSIS: {symbol}")
    print(f" Mode: {'MOCK' if mock else 'LIVE'}")
    print(f"{'='*60}\n")

    async def _internal():
        service = get_short_interest_service()
        
        # Force mock mode if requested
        if mock:
            service.quandl.mock = True
            service.av.mock = True

        try:
            analysis = await service.analyze_symbol(symbol)
            
            if not analysis:
                print(f"[-] FAILED: No analysis returned for {symbol}")
                return

            print(f"[+] SUCCESS: Analysis completed for {symbol}")
            print(f"    - Short Ratio: {analysis.short_ratio:.4f}")
            print(f"    - Days to Cover: {analysis.days_to_cover:.2f}")
            print(f"    - Squeeze Probability: {analysis.squeeze_probability:.2f}%")
            print(f"    - Risk Level: {analysis.risk_level}")
            print(f"    - Avg Daily Volume: {analysis.avg_daily_volume:,.0f}")
            
            print(f"\n[!] VERIFICATION PASSED")

        except Exception as e:
            print(f"[-] ERROR during test: {e}")
            logger.exception(e)

    asyncio.run(_internal())

if __name__ == "__main__":
    # Integration with system_control runner expects this signature
    import sys
    symbol = "TSLA"
    mock = False
    
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
    if "--mock" in sys.argv:
        mock = True
        
    asyncio.run(run_test_quandl(symbol, mock))
