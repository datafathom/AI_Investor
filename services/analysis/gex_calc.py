"""
Net Gamma Exposure (GEX) Calculator.
Calculates Market Maker hedging requirements.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GEXCalculator:
    """Calculates GEX from option chains."""
    
    def calculate_strike_gex(self, gamma: float, oi: int, spot_price: float) -> float:
        """Standard GEX formula: OI * Gamma * Spot * 100"""
        return oi * gamma * spot_price * 100
        
    def calculate_total_gex(self, chain_data: list) -> float:
        total = 0
        for strike in chain_data:
            c_gex = self.calculate_strike_gex(strike['c_gamma'], strike['c_oi'], strike['spot'])
            p_gex = self.calculate_strike_gex(strike['p_gamma'], strike['p_oi'], strike['spot'])
            total += (c_gex - p_gex) # Net GEX
        return total
