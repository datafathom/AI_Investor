import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TrustModificationGate:
    """Controls modification rights (withdrawals, amendments) based on trust type."""
    
    def can_perform_action(self, trust_type: str, action: str) -> Dict[str, Any]:
        """
        Policy:
        - REVOCABLE: All actions allowed (Fully modifiable).
        - IRREVOCABLE: Withdrawals/Amendments blocked (Estate tax exclusion).
        """
        t_type = trust_type.upper()
        act = action.upper()
        
        is_revocable = t_type == "REVOCABLE"
        
        # Only allow rebalancing/investing in Irrevocable; block withdrawals/amendments
        allowed_irrevocable = ["INVEST", "REBALANCE", "SELL"]
        
        is_allowed = is_revocable or (act in allowed_irrevocable)
        
        result_msg = "ACTION_ALLOWED" if is_allowed else "ACTION_BLOCKED_BY_LEGAL_ENTITY"
        
        if not is_allowed:
            logger.warning(f"LEGAL_ALERT: Blocked {action} on IRREVOCABLE trust. Grantor has surrendered control.")
            
        return {
            "is_allowed": is_allowed,
            "reason": result_msg,
            "trust_category": t_type
        }
