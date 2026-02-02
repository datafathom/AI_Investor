import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PolicyExitModeler:
    """
    Phase 177.4: Policy Loan Exit Strategy Modeler.
    Models accessing cash value via tax-free loans without lapsing the policy.
    """
    
    def simulate_retirement_draw(
        self,
        cash_value: Decimal,
        annual_loan: Decimal,
        loan_rate: Decimal,
        is_capped: bool = True
    ) -> Dict[str, Any]:
        """
        Policy: Ensure loan doesn't exceed 90% of cash value over 20 years.
        """
        current_cv = cash_value
        total_loan_balance = Decimal('0')
        years_sustained = 0
        
        for year in range(1, 21):
            total_loan_balance += annual_loan
            # Accrue interest on loan
            total_loan_balance *= (Decimal('1') + loan_rate)
            
            # Simplified CV growth (assumed 6%)
            current_cv *= Decimal('1.06')
            
            if total_loan_balance > (current_cv * Decimal('0.9')):
                break
            years_sustained = year
            
        logger.info(f"SIM_LOG: Policy loan strategy analyzed. Sustained: {years_sustained} years.")
        
        return {
            "years_sustained": years_sustained,
            "final_loan_balance": round(float(total_loan_balance), 2),
            "final_cash_value": round(float(current_cv), 2),
            "status": "SUSTAINABLE" if years_sustained >= 20 else "RISK_OF_LAPSE"
        }
