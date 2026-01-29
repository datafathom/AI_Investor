import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PPLIWithdrawalEngine:
    """Manages tax-free access to PPLI cash value via policy loans."""
    
    def calculate_max_loan(self, cash_value: float, cost_of_insurance_annual: float) -> Dict[str, Any]:
        """
        Policy: Allow loans up to 90% of cash value, ensuring buffer for 2 years of COI.
        """
        safe_buffer = cost_of_insurance_annual * 2
        max_loan = (cash_value - safe_buffer) * 0.90
        
        if max_loan < 0: max_loan = 0.0
        
        logger.info(f"INSURANCE_LOG: PPLI Max Loan: ${max_loan:,.2f} on ${cash_value:,.2f} cash value.")
        
        return {
            "max_safe_loan": round(float(max_loan), 2),
            "lapse_buffer_retained": round(float(safe_buffer), 2),
            "loan_to_value_pct": round(max_loan / cash_value, 4) if cash_value > 0 else 0
        }
