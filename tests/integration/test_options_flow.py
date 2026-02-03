"""
==============================================================================
FILE: scripts/runners/test_options_flow.py
ROLE: CLI Runner
PURPOSE: Execute and verify Phase 9 Options Flow Tracking logic.
==============================================================================
"""

import logging
from services.data.options_service import OptionsFlowService

logger = logging.getLogger(__name__)

def run_test_options_flow(symbol: str = "TSLA", mock: bool = False):
    """
    Runner function to test options flow ingestion and analysis.
    """
    logger.info(f"--- Testing Options Flow Tracking for {symbol} (Mock={mock}) ---")
    
    service = OptionsFlowService(mock=mock)
    
    logger.info(f"Fetching options chain for {symbol}...")
    chain = service.fetch_historical_options(symbol)
    
    if not chain:
        logger.error(f"Failed to fetch options chain for {symbol}. Check API Key/Limits.")
        return

    logger.info(f"Retrieved {len(chain)} contracts. Analyzing for unusual flow...")
    
    alerts = service.analyze_unusual_flow(chain)
    
    if not alerts:
        logger.info("No unusual flow detected with current heuristics.")
    else:
        logger.info(f"DETECTED {len(alerts)} UNUSUAL FLOW EVENTS:")
        for alert in alerts[:10]: # Print first 10
            print(f"[{alert['alert_type']}] {alert['type']} | Strike: {alert['strike']} | Exp: {alert['expiration']} | Vol: {alert['volume']} | OI: {alert['open_interest']}")

    sentiment = service.get_options_sentiment(symbol)
    logger.info(f"Overall Options Sentiment (P/C Ratio) for {symbol}: {sentiment:.2f}")

if __name__ == "__main__":
    run_test_options_flow()
