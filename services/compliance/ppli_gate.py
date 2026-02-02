import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PPLIEligibilityGate:
    """Strict KYC gate for Private Placement Life Insurance (PPLI)."""
    
    # Qualified Purchaser (QP) - SEC Standard
    MIN_NET_WORTH_QP = 5000000 # $5M net investments (simplified as NW for now)
    MIN_INSTITUTIONAL = 25000000 # $25M for entities
    
    def check_eligibility(self, user_id: str, net_worth: float, status: str = "INDIVIDUAL") -> Dict[str, Any]:
        """
        Enforce Accredited Investor vs Qualified Purchaser status.
        PPLI typically requires QP status.
        """
        is_qp = net_worth >= self.MIN_NET_WORTH_QP if status == "INDIVIDUAL" else net_worth >= self.MIN_INSTITUTIONAL
        
        logger.info(f"COMPLIANCE_LOG: PPLI Gate check for {user_id}. NW: ${net_worth:,.2f}. Status: {'PASSED' if is_qp else 'FAILED'}")
        
        return {
            "user_id": user_id,
            "is_eligible": is_qp,
            "accreditation_level": "QUALIFIED_PURCHASER" if is_qp else "RETAIL",
            "next_steps": ["PROCEED_TO_ILIT_SETUP"] if is_qp else ["UPGRADE_WEALTH_STRATEGY", "RETAIL_WRAPPERS_ONLY"]
        }

    def check_mec_status(self, premium_paid: float, seven_pay_limit: float) -> Dict[str, Any]:
        """
        Phase 168.3: 7-Pay Test. If premiums > limit, it's a MEC.
        """
        is_mec = premium_paid > seven_pay_limit
        
        if is_mec:
            logger.warning("COMPLIANCE_ALERT: MEC status triggered. Loans will be taxable.")
            
        return {
            "is_mec": is_mec,
            "status": "MEC" if is_mec else "NON_MEC",
            "loan_tax_advantage": not is_mec,
            "headroom": max(0.0, seven_pay_limit - premium_paid)
        }
