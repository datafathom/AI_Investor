import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SafeWithdrawalService:
    """Calculates safe annual withdrawal amounts based on the 4% rule and dynamic factors."""
    
    def calculate_withdrawal(self, portfolio_value: float, cape_ratio: float) -> Dict[str, Any]:
        """
        Logic: 
        - CAPE > 30 (Overvalued): Reduce to 3.0%
        - 15 < CAPE < 30 (Fair): Standard 4.0%
        - CAPE < 15 (Undervalued): Increase to 5.0%
        """
        if cape_ratio > 30:
            rate = 0.03
        elif cape_ratio < 15:
            rate = 0.05
        else:
            rate = 0.04
            
        amount = portfolio_value * rate
        
        logger.info(f"RET_LOG: Safe withdrawal at CAPE {cape_ratio:.1f}: {rate*100:.1f}% (${amount:,.2f})")
        
        return {
            "withdrawal_rate": rate,
            "annual_amount": round(amount, 2),
            "monthly_amount": round(amount / 12, 2),
            "valuation_status": "HIGH" if rate == 0.03 else ("LOW" if rate == 0.05 else "NORMAL")
        }
