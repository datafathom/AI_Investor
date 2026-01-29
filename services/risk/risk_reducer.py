import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RiskReducerService:
    """Manages emergency risk reduction as deadlines approach."""
    
    def evaluate_deadline_risk(self, months_remaining: int) -> Dict[str, Any]:
        """
        Policy: If < 12 months, move 25% of goal amount to cash/ultra-short bonds.
        """
        is_emergency = months_remaining <= 12
        if is_emergency:
            logger.warning(f"RISK_ALERT: Goal deadline nearing! {months_remaining} months left. Triggering RISK_REDUCTION.")
            
        return {
            "months_left": months_remaining,
            "action": "FORCE_CASH_OFFSET" if is_emergency else "NONE",
            "cash_buffer_suggested": 0.25 if is_emergency else 0.0
        }
