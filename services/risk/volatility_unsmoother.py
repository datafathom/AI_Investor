import logging
from typing import List
from services.private_markets.premium_optimizer import PremiumOptimizer

logger = logging.getLogger(__name__)

class VolatilityUnsmoother:
    """
    Phase 172.2: Return 'Unsmoothing' Algorithm.
    Uses Geltner Index to calculate true underlying volatility.
    """
    
    def __init__(self):
        self.optimizer = PremiumOptimizer()

    def get_true_volatility(self, smoothed_returns: List[float], rho: float = 0.5) -> float:
        """
        Calculates standard deviation of unsmoothed returns.
        """
        unsmoothed = self.optimizer.unsmooth_returns(smoothed_returns, rho)
        if not unsmoothed:
            return 0.0
            
        import statistics
        return statistics.stdev(unsmoothed) if len(unsmoothed) > 1 else 0.0
