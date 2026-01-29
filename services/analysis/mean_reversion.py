import logging
from typing import List, Optional
from decimal import Decimal
import statistics

logger = logging.getLogger(__name__)

class MeanReversionService:
    """
    Detects mean-reversion opportunities based on statistical deviations.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MeanReversionService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("MeanReversionService initialized")

    def calculate_mean_and_std(self, prices: List[float]) -> dict:
        """Calculate rolling mean and standard deviation."""
        if len(prices) < 2:
            return {"mean": 0, "std": 0}
        
        mean = statistics.mean(prices)
        std = statistics.stdev(prices)
        return {"mean": mean, "std": std}

    def calculate_z_score(self, current_price: float, mean: float, std: float) -> float:
        """Calculate Z-score (standard deviations from mean)."""
        if std == 0:
            return 0
        return (current_price - mean) / std

    def detect_extreme_extension(self, prices: List[float], threshold: float = 2.0) -> Optional[str]:
        """
        Detect if price is extended beyond threshold standard deviations.
        Returns 'OVERBOUGHT', 'OVERSOLD', or None.
        """
        if len(prices) < 20:
            return None
            
        stats = self.calculate_mean_and_std(prices[:-1])  # Use all but last for calculation
        z_score = self.calculate_z_score(prices[-1], stats["mean"], stats["std"])
        
        if z_score >= threshold:
            logger.info(f"OVERBOUGHT detected: Z-score = {z_score:.2f}")
            return "OVERBOUGHT"
        elif z_score <= -threshold:
            logger.info(f"OVERSOLD detected: Z-score = {z_score:.2f}")
            return "OVERSOLD"
        
        return None

    def calculate_fair_value(self, prices: List[float], window: int = 20) -> float:
        """Calculate fair value as rolling mean."""
        if len(prices) < window:
            return statistics.mean(prices) if prices else 0
        return statistics.mean(prices[-window:])
