import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TrueSharpeCalculator:
    """
    Phase 172.4: True Sharpe Ratio (Unsmoothed) Service.
    Calculates Sharpe using the unsmoothed volatility of private assets.
    """
    
    def calculate_true_sharpe(self, annual_return: float, risk_free_rate: float, true_volatility: float) -> Dict[str, Any]:
        """
        Sharpe = (Ret - RF) / True Vol.
        """
        excess_return = annual_return - risk_free_rate
        sharpe = excess_return / true_volatility if true_volatility > 0 else 0.0
        
        logger.info(f"PERF_LOG: True Sharpe (Unsmoothed): {sharpe:.2f}")
        
        return {
            "excess_return": round(excess_return, 4),
            "true_volatility": round(true_volatility, 4),
            "true_sharpe": round(sharpe, 2)
        }
