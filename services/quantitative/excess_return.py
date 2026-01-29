import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExcessReturnCalculator:
    """Computes returns in excess of the risk-free rate."""
    
    def calculate_excess_ret(self, portfolio_ret: float, rfr_rate: float) -> float:
        """
        Policy: Arithmetically subtract the RFR.
        """
        excess = portfolio_ret - rfr_rate
        
        logger.info(f"QUANT_LOG: Excess Return: {excess:.2%} (Portfolio: {portfolio_ret:.2%}, RFR: {rfr_rate:.2%})")
        return round(float(excess), 6)

    def validate_rfr_selection(self, strategy_duration: str, rfr_curve: Dict[str, float]) -> float:
        """
        Policy: Select appropriate T-Bill/Note based on strategy intent.
        """
        if strategy_duration.upper() == "CASH_LIKE":
            return rfr_curve.get("yield_3mo", 0.0)
        return rfr_curve.get("yield_10yr", 0.0)
