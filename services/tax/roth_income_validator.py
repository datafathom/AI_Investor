import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RothIncomeValidator:
    """Validates Roth IRA eligibility based on MAGI."""
    
    # 2025 Limits
    LIMITS = {
        "SINGLE": {"limit": 146000, "phase_out": 161000},
        "MARRIED_JOINT": {"limit": 230000, "phase_out": 240000}
    }

    def validate_eligibility(self, magi: float, filing_status: str) -> Dict[str, Any]:
        status_limits = self.LIMITS.get(filing_status, self.LIMITS["SINGLE"])
        
        if magi < status_limits["limit"]:
            return {"allowed": True, "type": "FULL", "message": "Full contribution allowed."}
        
        if magi < status_limits["phase_out"]:
            return {"allowed": True, "type": "PARTIAL", "message": "Reduced contribution allowed (phase-out)."}
            
        logger.warning(f"ELIGIBILITY_LOG: MAGI ${magi:,.2f} exceeds Roth limits for {filing_status}")
        return {
            "allowed": False, 
            "type": "NONE", 
            "message": "Income exceeds Roth limits. Consider Backdoor Roth.",
            "suggest_backdoor": True
        }
