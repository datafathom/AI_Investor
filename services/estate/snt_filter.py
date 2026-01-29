
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SNTDistributionFilter:
    """
    Ensures that Special Needs Trust (SNT) distributions do not disqualify 
    the beneficiary from SSI (Supplemental Security Income) or Medicaid.
    """
    
    # Categories that are generally safe if paid directly to vendors
    ALLOWED_CATEGORIES = [
        "MEDICAL_REHABILITATION",
        "EDUCATION",
        "TRANSPORTATION",
        "ELECTRONICS_FURNISHINGS",
        "TRAVEL_ENTERTAINMENT",
        "LEGAL_SERVICE",
        "DENTAL_VISUAL"
    ]
    
    # Categories that cause ISM (In-Kind Support and Maintenance) reduction or disqualification
    RESTRICTED_CATEGORIES = [
        "SHELTER_RENT",
        "FOOD_GROCERIES",
        "CASH_DIRECT"
    ]
    
    def validate_distribution(
        self,
        payee_type: str,        # 'VENDOR' or 'BENEFICIARY'
        expense_category: str,  # e.g. 'EDUCATION', 'FOOD_GROCERIES'
        amount: float
    ) -> Dict[str, Any]:
        """
        Validate the distribution request.
        """
        logger.info(f"SNT Validation: Payee={payee_type}, Category={expense_category}, Amount=${amount}")
        
        status = "ALLOWED"
        reason = "Meets SNT safe harbor guidelines."
        risk_level = "LOW"
        
        if payee_type == "BENEFICIARY":
            status = "DENIED"
            reason = "Cash distributions directly to beneficiary will disqualify them from SSI/Medicaid."
            risk_level = "CRITICAL"
        elif expense_category in self.RESTRICTED_CATEGORIES:
            status = "WARNING"
            reason = f"Payment for {expense_category} will cause an ISM reduction in SSI benefits (In-Kind Support and Maintenance)."
            risk_level = "HIGH"
        elif expense_category not in self.ALLOWED_CATEGORIES:
            status = "MANUAL_REVIEW"
            reason = "Category not pre-approved. Requires trustee review."
            risk_level = "MEDIUM"
            
        return {
            "status": status,
            "reason": reason,
            "risk_level": risk_level,
            "amount": amount
        }
