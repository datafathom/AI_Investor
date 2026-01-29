import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class REITPayoutValidator:
    """Validates that a REIT is distributing the required taxable income (usually 90%)."""
    
    MIN_REQUIREMENT = 0.90

    def validate_payout(self, taxable_income: float, dividends_paid: float) -> Dict[str, Any]:
        if taxable_income <= 0: return {"is_compliant": True, "ratio": 0.0}
        
        ratio = dividends_paid / taxable_income
        is_compliant = ratio >= self.MIN_REQUIREMENT
        
        if not is_compliant:
            logger.error(f"REIT_ALERT: Distribution FAILURE! Ratio {ratio:.2%} < required {self.MIN_REQUIREMENT:.2%}")
        else:
            logger.info(f"REIT_LOG: Payout compliant at {ratio:.2%}")
            
        return {
            "is_compliant": is_compliant,
            "actual_ratio": round(ratio, 4),
            "required_ratio": self.MIN_REQUIREMENT,
            "shortfall": round(max(0, (taxable_income * self.MIN_REQUIREMENT) - dividends_paid), 2)
        }
