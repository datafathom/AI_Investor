"""
Tax Forecaster.
Compares Roth vs Traditional outcomes.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TaxForecaster:
    """Forecasts tax implications."""
    
    @staticmethod
    def compare_strategies(principal: float, years: int, growth: float, current_tax: float, future_tax: float) -> Dict[str, float]:
        # Traditional (Pre-tax)
        trad_future = principal * ((1 + growth) ** years)
        trad_net = trad_future * (1 - future_tax)
        
        # Roth (Post-tax)
        roth_principal = principal * (1 - current_tax)
        roth_net = roth_principal * ((1 + growth) ** years)
        
        return {
            "traditional_net": round(trad_net, 2),
            "roth_net": round(roth_net, 2),
            "better_strategy": "ROTH" if roth_net > trad_net else "TRADITIONAL"
        }
