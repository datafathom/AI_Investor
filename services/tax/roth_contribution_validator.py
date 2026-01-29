import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RothContributionValidator:
    """Validates if a user can make direct Roth IRA contributions based on income."""
    
    # 2024 Limits (Single)
    SINGLE_PHASE_OUT_START = 146000
    SINGLE_MAX_INCOME = 161000

    def validate_direct_contribution(self, income: float, marital_status: str = "SINGLE") -> Dict[str, Any]:
        """
        Logic: 
        - Below Phase Out: ALLOWED
        - In Phase Out: PARTIAL (Reduced)
        - Above Max: BLOCKED (Suggest Backdoor)
        """
        if income < self.SINGLE_PHASE_OUT_START:
            status = "ALLOWED"
        elif income < self.SINGLE_MAX_INCOME:
            status = "PARTIAL"
        else:
            status = "BLOCKED"
            
        logger.info(f"TAX_LOG: Direct Roth check for ${income:,.2f} -> {status}")
        
        return {
            "status": status,
            "suggestion": "BACKDOOR_ROTH" if status == "BLOCKED" else "DIRECT"
        }
