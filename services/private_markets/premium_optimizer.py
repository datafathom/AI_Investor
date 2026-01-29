import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PremiumOptimizer:
    """
    Manages Illiquidity Premium calculations and return unsmoothing.
    Implements Geltner-style unsmoothing for private asset appraisals.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PremiumOptimizer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("PremiumOptimizer initialized")

    def calculate_illiquidity_premium(self, private_irr: Decimal, public_equiv_irr: Decimal) -> Dict[str, Any]:
        """
        Policy: Target premium is 300-500bps for illiquid lock-ups.
        """
        premium_bps = (private_irr - public_equiv_irr) * Decimal('10000')
        
        return {
            "premium_bps": int(premium_bps),
            "is_sufficient": premium_bps >= Decimal('300'),
            "alpha_vs_benchmark": round(private_irr - public_equiv_irr, 4)
        }

    def unsmooth_returns(self, smoothed_returns: List[float], rho: float = 0.5) -> List[float]:
        """
        Geltner Formula: True_R(t) = [Smoothed_R(t) - rho * Smoothed_R(t-1)] / (1 - rho)
        Exposes the true volatility hidden by quarterly appraisals.
        """
        if len(smoothed_returns) < 2:
            return smoothed_returns
            
        unsmoothed = [smoothed_returns[0]] # First remains same
        
        for i in range(1, len(smoothed_returns)):
            r_true = (smoothed_returns[i] - (rho * smoothed_returns[i-1])) / (1 - rho)
            unsmoothed.append(round(r_true, 6))
            
        logger.info(f"RISK_LOG: Unsmoothed {len(unsmoothed)} data points (rho={rho}).")
        return unsmoothed
