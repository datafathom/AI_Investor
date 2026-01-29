import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FFOCalculator:
    """Calculates Funds From Operations (FFO) for REITs."""
    
    def calculate_ffo(self, net_income: float, depreciation: float, gains_on_sales: float) -> float:
        """
        Standard REIT FFO Formula: 
        FFO = Net Income + Depreciation + Amortization - Gains on Sales of Property
        """
        ffo = net_income + depreciation - gains_on_sales
        logger.info(f"REIT_LOG: FFO calculated: ${ffo:,.2f}")
        return round(float(ffo), 2)

    def calculate_affo(self, ffo: float, recurring_cap_ex: float) -> float:
        """
        Adjusted FFO (AFFO) subtracts maintenance cap-ex for truer cash flow.
        """
        affo = ffo - recurring_cap_ex
        logger.info(f"REIT_LOG: AFFO calculated: ${affo:,.2f}")
        return round(float(affo), 2)
