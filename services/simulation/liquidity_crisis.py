"""
Liquidity Crisis Simulator.
Stress-tests exit slippage during high volatility.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LiquidityCrisisSim:
    """Simulates 'Bank Run' scenarios."""
    
    def simulate_exit(self, portfolio_value: float, vol_spike: float) -> Dict[str, Any]:
        """
        vol_spike: multiplier for spread widening (e.g. 5.0x)
        """
        base_slippage = 0.0010 # 10bps
        stressed_slippage = base_slippage * vol_spike
        
        exit_cost = portfolio_value * stressed_slippage
        
        return {
            "slippage_bps": round(stressed_slippage * 10000, 1),
            "exit_cost_usd": round(exit_cost, 2),
            "can_exit_portfolio": stressed_slippage < 0.05
        }
