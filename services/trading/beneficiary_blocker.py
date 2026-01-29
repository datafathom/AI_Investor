
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BeneficiaryOrderBlocker:
    """
    Prevents beneficiaries of a Blind Trust from placing orders.
    Trades must be performed only by the Trustee.
    """
    
    def validate_order(self, user_role: str, trust_type: str) -> Dict[str, Any]:
        """
        Validates if the user is allowed to place an order.
        """
        logger.info(f"Order Validation: Role={user_role}, TrustType={trust_type}")
        
        if trust_type == "BLIND" and user_role == "BENEFICIARY":
            logger.warning("BLIND TRUST VIOLATION: Beneficiary attempted to place a trade.")
            return {
                "allowed": False,
                "reason": "Beneficiaries of Blind Trusts cannot direct trades to avoid conflicts of interest.",
                "action": "BLOCK_ORDER"
            }
            
        return {
            "allowed": True,
            "reason": "Order authorized for Trustee/Advisor."
        }
