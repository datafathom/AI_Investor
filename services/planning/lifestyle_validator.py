import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LifestyleValidator:
    """Checks if portfolio growth offsets inflation for social class maintenance."""
    
    def validate_purchasing_power(self, current_net_worth: float, horizon_years: int, inflation_rate: float, portfolio_return: float) -> Dict[str, Any]:
        """
        Calculates if the real net worth increases or decreases over the horizon.
        """
        # Nominal Future Value
        nominal_fv = current_net_worth * (1 + portfolio_return)**horizon_years
        
        # Real Future Value (inflation adjusted)
        real_fv = nominal_fv / (1 + inflation_rate)**horizon_years
        
        status = "MAINTAINED" if real_fv >= current_net_worth else "DECLINING"
        
        logger.info(f"PLAN_LOG: {horizon_years}Y Outlook: Real Value ${real_fv:,.2f} ({status})")
        
        return {
            "is_maintained": real_fv >= current_net_worth,
            "real_future_value": round(real_fv, 2),
            "real_growth_pct": round((real_fv - current_net_worth) / current_net_worth, 4),
            "status": status
        }
