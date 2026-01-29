"""
Rental Yield Calculator.
Calculates net ROI on physical investment properties.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RentalYieldCalc:
    """Calculates property caps and yields."""
    
    def calculate_net_yield(self, rent: float, mortgage: float, tax: float, maintenance: float, equity: float) -> float:
        net_income = rent - mortgage - tax - maintenance
        if equity <= 0: return 0.0
        
        yield_pct = (net_income * 12) / equity
        logger.info(f"REAL_ESTATE_LOG: Calculated {(yield_pct*100):.2f}% target yield.")
        return yield_pct
