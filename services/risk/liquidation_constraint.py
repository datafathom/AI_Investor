import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LiquidationConstraint:
    """
    Blocks new investment allocations when emergency fund levels are unsafe.
    """
    
    CRITICAL_THRESHOLD = 3.0 # months

    def check_trade_allowed(self, months_coverage: float, trade_type: str) -> Dict[str, Any]:
        """
        Policy: Block buy orders if coverage < 3 months.
        Sell orders (to increase cash) are always allowed.
        """
        if months_coverage < self.CRITICAL_THRESHOLD and trade_type == "BUY":
            logger.warning(f"CONSTRAINT_BLOCK: Buy order blocked. Emergency fund coverage ({months_coverage} mo) below limit.")
            return {
                "allowed": False,
                "reason": "Emergency fund coverage is below 3-month threshold. Capital preservation mandatory.",
                "code": "LIQUIDITY_LOCK_ACTIVE"
            }
            
        return {"allowed": True}

    def get_suggested_remediation(self, target_cash: float, current_cash: float) -> str:
        deficit = target_cash - current_cash
        return f"Immediate cash injection of ${deficit:,.2f} required to unlock trading."
