import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PrincipalGateService:
    """Enforces boundaries to prevent tapping into the portfolio principal."""
    
    def validate_withdrawal_intent(self, portfolio_value: float, initial_principal: float, intent_amount: float) -> Dict[str, Any]:
        """
        Checks if the requested withdrawal will eat into the original principal.
        """
        excess_growth = portfolio_value - initial_principal
        
        # If principal is already underwater, any withdrawal taps principal.
        is_tapping = intent_amount > excess_growth or excess_growth <= 0
        
        if is_tapping:
            logger.warning(f"RET_ALERT: Withdrawal of ${intent_amount:,.2f} taps into PRINCIPAL! Excess growth only ${max(0, excess_growth):,.2f}")
            
        return {
            "is_tapping_principal": is_tapping,
            "excess_growth_available": round(max(0, excess_growth), 2),
            "safe_limit": round(max(0, excess_growth), 2)
        }
