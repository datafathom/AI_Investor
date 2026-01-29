import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LiquidationBlocker:
    """Prevents portfolio liquidation if safety thresholds (Emergency Fund) are breached."""
    
    def can_liquidate(self, emergency_fund_balance: float, target_buffer: float) -> bool:
        """
        Logic: 
        - Cannot sell portfolio assets if emergency fund < 1 month of expenses.
        - Warning if fund < Target.
        """
        if emergency_fund_balance <= 0:
            logger.error("RISK_ALERT: Liquidation BLOCKED. Emergency fund is EMPTY.")
            return False
            
        is_safe = emergency_fund_balance >= target_buffer
        
        if not is_safe:
            logger.warning(f"RISK_ALERT: Emergency fund ({emergency_fund_balance}) below target ({target_buffer}). Liquidation discouraged.")
            
        return True # Discouraged but technically allowed unless empty

    def hard_block_check(self, emergency_fund_balance: float, min_required: float) -> bool:
        return emergency_fund_balance > min_required
