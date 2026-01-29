"""
Crack Spread Monitor.
Calculates refiner margins (Gasoline/Distillates vs Crude).
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CrackSpreadMonitor:
    """Calculates oil refining margins."""
    
    def calculate_321_spread(self, crude_price: float, gas_price: float, heat_oil_price: float) -> float:
        """Standard 3:2:1 spread formula."""
        # 3 barrels of crude -> 2 gas + 1 distillate
        margin = (2 * gas_price + 1 * heat_oil_price) - (3 * crude_price)
        return round(margin / 3, 2)
