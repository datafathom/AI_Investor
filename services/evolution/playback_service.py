"""
==============================================================================
FILE: services/evolution/playback_service.py
ROLE: Chronological Auditor
PURPOSE:
    Facilitate the "Re-run" of trade cycles for specific agent genomes
    to visualize performance in a virtual sandbox.
    
    1. Fetch historical price data.
    2. Map genes to strategy parameters.
    3. Run the Backtest Engine in "Playback" mode.

CONTEXT: 
    Part of Sprint 4: Evolution Lab.
==============================================================================
"""

import logging
from typing import Dict, List, Any, Optional
from services.analysis.backtest_engine import get_backtester, BacktestResult
from services.analysis.genetic_distillery import Genome

logger = logging.getLogger(__name__)

class PlaybackService:
    """
    Handles re-running historical data for a specific genome set.
    """

    def __init__(self):
        self.backtester = get_backtester()

    def run_playback(self, 
                    genes: Dict[str, Any], 
                    price_data: List[Dict[str, Any]], 
                    initial_cash: float = 100000.0) -> BacktestResult:
        """
        Runs a backtest simulation using the provided genes as strategy parameters.
        """
        logger.info(f"Starting playback for genes: {genes}")
        
        # Simple mapping function: use RSI genes if they exist
        def playback_strategy(ts, positions, cash, current_prices):
            orders = []
            rsi_period = genes.get("rsi_period", 14)
            rsi_buy = genes.get("rsi_buy", 30)
            rsi_sell = genes.get("rsi_sell", 70)
            
            # Simple RSI-like mock logic for demonstration
            # In a real scenario, this would call a refined strategy module
            price = current_prices.get("SPY", 0)
            if price > 0:
                # Mock signal based on RSI genes
                if price < 400 and rsi_buy > 25: # "Oversold" mock
                    orders.append({"symbol": "SPY", "side": "BUY", "quantity": 10})
                elif price > 480 and rsi_sell < 75: # "Overbought" mock
                    orders.append({"symbol": "SPY", "side": "SELL", "quantity": 10})
                    
            return orders

        result = self.backtester.run(price_data, playback_strategy)
        return result

def get_playback_service() -> PlaybackService:
    return PlaybackService()
