import logging
import numpy as np
from typing import List

logger = logging.getLogger(__name__)

class TrackingErrorCalculator:
    """Measures how closely a portfolio follows its benchmark."""
    
    def calculate_tracking_error(self, portfolio_returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Tracking Error = Standard Deviation of (Rp - Rb)
        """
        if len(portfolio_returns) != len(benchmark_returns) or len(portfolio_returns) < 2:
            return 0.0
            
        excess_returns = np.array(portfolio_returns) - np.array(benchmark_returns)
        # Annualized standard deviation of excess returns
        te = np.std(excess_returns, ddof=1) * np.sqrt(252)
        
        logger.info(f"QUANT_LOG: Tracking Error: {te:.2%}")
        return round(float(te), 4)
