import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LeverageBlocker:
    """Blocks trust assets from being used as collateral or for margin loans."""
    
    def can_pledge_as_collateral(self, trust_type: str, is_spendthrift: bool) -> Dict[str, Any]:
        """
        Policy: If is_spendthrift or IRREVOCABLE, pledging is strictly forbidden.
        """
        t_type = trust_type.upper()
        # Revocable non-spendthrift is essentially the Grantor's asset, others are shielded.
        can_pledge = (t_type == "REVOCABLE") and (not is_spendthrift)
        
        if not can_pledge:
            logger.warning(f"COMPLIANCE_ALERT: Blocked collateral pledge. Trust {trust_type} (Spendthrift: {is_spendthrift}) protects corpus from liens.")
            
        return {
            "can_pledge": can_pledge,
            "shield_status": "ACTIVE" if not can_pledge else "INACTIVE",
            "reason": "SPENDTHRIFT_PROTECTION_ENABLED" if not can_pledge else "STANDARD_RLT_CONTROL"
        }
