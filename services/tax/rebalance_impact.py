"""
Tax Impact Estimator.
Estimates cap gains tax before rebalancing trades.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TaxImpactEstimator:
    """Calculates potential tax liability of a rebalance."""
    
    def estimate_impact(self, ticker: str, shares_to_sell: int, cost_basis: float, current_price: float) -> float:
        gain = (current_price - cost_basis) * shares_to_sell
        if gain <= 0: return 0.0
        
        tax_bill = gain * 0.20 # Standard long-term rate
        logger.info(f"TAX_EST: Selling {ticker} triggers ${tax_bill:.2f} in tax.")
        return tax_bill
