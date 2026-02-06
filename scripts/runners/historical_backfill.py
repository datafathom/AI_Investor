"""
==============================================================================
FILE: scripts/runners/historical_backfill.py
ROLE: CLI Runner
PURPOSE: Dispatches requests to HistoricalLoader for backfilling data.
USAGE: python cli.py backfill-history --symbol [TICKER] --size [compact|full]
INPUT/OUTPUT:
    - Input: symbol (str), size (str)
    - Output: Success/Failure status printed to console.
==============================================================================
"""

import logging
from services.data.historical_loader import HistoricalLoader

logger = logging.getLogger(__name__)

def run_historical_backfill(symbol: str = "SPY", size: str = "compact", **kwargs):
    """
    Runner function to execute historical data backfill.
    """
    print(f"--- Starting Historical Backfill for {symbol} ({size}) ---")
    
    loader = HistoricalLoader()
    
    loader = HistoricalLoader()
        
    success = loader.load_daily_history(symbol, outputsize=size)
    
    if success:
        print(f"Successfully completed backfill for {symbol}.")
    else:
        print(f"Backfill failed for {symbol}. Check logs for details.")
        
    return success
