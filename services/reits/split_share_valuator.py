import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SplitShareValuator:
    """Valuates 'split-share' REIT structures (Preferred vs Common allocations)."""
    
    def calculate_yield_spread(self, preferred_yield: float, common_yield: float) -> float:
        """
        Preferred shares usually have higher priority but lower growth.
        """
        spread = preferred_yield - common_yield
        logger.info(f"REIT_LOG: Yield Spread (Pref - Common): {spread*100:.2f}%")
        return round(float(spread), 4)

    def assess_risk_profile(self, LTV: float) -> str:
        """Loan-to-Value assessment."""
        if LTV < 0.40: return "CONSERVATIVE"
        if LTV < 0.60: return "MODERATE"
        return "AGGRESSIVE"
