import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PenaltyCalculator529:
    """Calculates tax and penalties for non-qualified 529 distributions."""
    
    PENALTY_RATE = 0.10 # 10% IRS Penalty on earnings

    def calculate_liability(self, total_distribution: float, earnings_portion: float, income_tax_bracket: float) -> Dict[str, Any]:
        """
        Policy: Penalty and income tax apply ONLY to the earnings portion of the withdrawal.
        """
        irs_penalty = earnings_portion * self.PENALTY_RATE
        income_tax = earnings_portion * income_tax_bracket
        
        total_hit = irs_penalty + income_tax
        net_amount = total_distribution - total_hit
        
        logger.info(f"TAX_LOG: Non-qualified withdrawal penalty: ${irs_penalty:,.2f}, Tax: ${income_tax:,.2f}. Net: ${net_amount:,.2f}")
        
        return {
            "earnings_portion": round(earnings_portion, 2),
            "irs_penalty": round(irs_penalty, 2),
            "income_tax": round(income_tax, 2),
            "total_tax_hit": round(total_hit, 2),
            "net_to_client": round(net_amount, 2)
        }
