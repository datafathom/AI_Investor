import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class YieldWithdrawalCalculator:
    """Calculates withdrawals that preserve real principal by using Yield - Inflation."""
    
    def calculate_yield_safe_amount(self, portfolio_value: float, portfolio_yield: float, current_inflation: float) -> Dict[str, Any]:
        """
        Policy: Sustainable rate is Yield % minus Inflation %.
        If yield < inflation, safe withdrawal is effectively 0 to preserve real power.
        """
        real_yield = portfolio_yield - current_inflation
        safe_rate = max(0, real_yield)
        
        annual_amount = portfolio_value * safe_rate
        
        logger.info(f"RET_LOG: Yield-based check: Yield {portfolio_yield:.2%}, Inflation {current_inflation:.2%}. Safe rate: {safe_rate:.2%}")
        
        return {
            "portfolio_yield": round(portfolio_yield, 4),
            "real_yield": round(real_yield, 4),
            "safe_withdrawal_rate": round(safe_rate, 4),
            "annual_amount": round(annual_amount, 2),
            "preserves_principal": True
        }
