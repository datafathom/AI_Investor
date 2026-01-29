import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AllowanceEngine:
    """Calculates and gates trust distributions based on Spendthrift rules."""
    
    def validate_withdrawal(self, requested_amount: float, monthly_limit: float, 
                            current_month_total: float, is_emergency: bool = False) -> Dict[str, Any]:
        """
        Policy: 
        1. Block if (requested + current) > monthly_limit.
        2. Allow if emergency override is active and approved.
        """
        projected_total = current_month_total + requested_amount
        
        is_allowed = projected_total <= monthly_limit
        if is_emergency:
            is_allowed = True # Simplification: emergency bypasses limit
            
        if not is_allowed:
            logger.warning(f"LEGAL_ALERT: Spendthrift block! Beneficiary requested ${requested_amount:,.2f} exceeding monthly limit of ${monthly_limit:,.2f}.")
            
        return {
            "is_approved": is_allowed,
            "approved_amount": round(requested_amount, 2) if is_allowed else 0.0,
            "remaining_budget": round(monthly_limit - projected_total, 2) if is_allowed else round(monthly_limit - current_month_total, 2)
        }
