"""
Allocation Guard.
Enforces the 1% risk rule per trade.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AllocationGuard:
    """Enforces 1% risk rule."""
    
    MAX_RISK_PCT = 0.01
    
    def validate_trade(self, equity: float, risk_amount: float) -> Dict[str, Any]:
        """Validate if trade fits within 1% risk."""
        if equity <= 0:
            return {"valid": False, "reason": "No equity"}
            
        risk_pct = risk_amount / equity
        
        if risk_pct > self.MAX_RISK_PCT:
            logger.warning(f"RISK_VIOLATION: Attempted {risk_pct*100:.2f}% risk. Max {self.MAX_RISK_PCT*100}%")
            return {
                "valid": False,
                "reason": f"Risk {risk_pct*100:.2f}% exceeds 1% limit",
                "max_allowed": equity * self.MAX_RISK_PCT
            }
            
        return {"valid": True, "risk_pct": risk_pct}
