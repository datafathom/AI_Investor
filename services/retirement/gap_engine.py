import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RetirementGapEngine:
    """Calculates gap between current trajectory and retirement goals."""
    
    def calculate_gap(self, current_balance: float, target_monthly_income: float, years_to_ret: float) -> Dict[str, Any]:
        # Required balance (4% rule)
        required_balance = target_monthly_income * 12 * 25
        
        # Simple projection (6% growth net of infl)
        projected_balance = current_balance * (1.06)**years_to_ret
        
        gap = required_balance - projected_balance
        
        logger.info(f"GAP_LOG: Required: ${required_balance:,.0f}, Proj: ${projected_balance:,.0f}, Gap: ${gap:,.0f}")
        
        return {
            "required_balance": round(required_balance, 2),
            "projected_balance": round(projected_balance, 2),
            "gap": round(max(0, gap), 2),
            "surplus": round(max(0, -gap), 2),
            "target_met": projected_balance >= required_balance
        }
