import logging
import numpy as np
from typing import List

logger = logging.getLogger(__name__)

class SharpeRatioCalculator:
    """
    Calculates the Sharpe Ratio: (Rp - Rf) / sigma_p.
    Rp: Portfolio Annualized Return
    Rf: Risk-Free Rate
    sigma_p: Portfolio Annualized Standard Deviation
    """
    
    def calculate(self, returns: List[float], risk_free_rate: float) -> float:
        """
        Calculates annualized Sharpe Ratio from sub-annual returns (e.g. daily).
        Assumes 252 trading days.
        """
        if len(returns) < 2:
            logger.error("QUANT_LOG: Insufficient data for Sharpe calculation.")
            return 0.0
            
        # Annualize Mean Return
        mean_ret = np.mean(returns) * 252
        
        # Annualize Volatility (Std Dev)
        vol = np.std(returns) * np.sqrt(252)
        
        if vol == 0:
            return 0.0
            
        sharpe = (mean_ret - risk_free_rate) / vol
        
        logger.info(f"QUANT_LOG: Sharpe Calculated: {sharpe:.4f} (Mean: {mean_ret:.2%}, Vol: {vol:.2%})")
        return round(float(sharpe), 4)
