import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FeeTierValidator:
    """
    Phase 175.5: Institutional Pricing Tier Validator.
    Verifies that the MFO is getting the lowest expense ratios across funds.
    """
    
    def audit_fee_tier(self, fund_id: str, current_bps: int, retail_bps: int, institutional_bps: int) -> Dict[str, Any]:
        """
        Policy: Ensure current_bps <= institutional_bps.
        """
        is_institutional = current_bps <= institutional_bps
        leakage_bps = max(0, current_bps - institutional_bps)
        
        if leakage_bps > 0:
            logger.warning(f"COMPLIANCE_LOG: Fee leakage detected on {fund_id}. {leakage_bps}bps above institutional floor.")
            
        return {
            "fund_id": fund_id,
            "status": "VALID_INSTITUTIONAL" if is_institutional else "RENEGOTIATION_REQUIRED",
            "leakage_bps": leakage_bps,
            "annual_savings_locked": retail_bps - current_bps
        }
