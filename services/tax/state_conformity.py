
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class StateConformityValidator:
    """
    Check if a state follows federal 'Qualified Expense' rules.
    (e.g., K-12 tuition or Student Loan repayments).
    """
    
    # States that do NOT conform to K-12 529 usage
    NON_CONFORMING_K12 = ["IL", "MN", "NY", "PA"]
    
    def validate_conformity(self, state: str, expense_type: str) -> Dict[str, Any]:
        """
        Returns tax risk for specific expense types.
        """
        risk = "NONE"
        if expense_type == "K12_TUITION" and state in self.NON_CONFORMING_K12:
            risk = "TAXABLE_AT_STATE_LEVEL"
            
        logger.info(f"State Conformity: {state} / {expense_type} -> Risk: {risk}")
        
        return {
            "state": state,
            "expense_type": expense_type,
            "conformity_risk": risk,
            "action": "CONSULT_TAX_ADVISOR" if risk != "NONE" else "PROCEED"
        }
