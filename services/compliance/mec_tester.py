import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MECTester:
    """
    Performs the '7-Pay Test' for Private Placement Life Insurance (PPLI).
    Ensures premiums are not over-funded, which would turn the policy into a 
    taxable Modified Endowment Contract (MEC).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MECTester, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("MECTester initialized")

    def run_7pay_test(self, policy_limit_annual: Decimal, premiums_paid_ytd: Decimal) -> Dict[str, Any]:
        """
        Policy: If YTD premiums > 7-pay limit, Policy = MEC.
        """
        is_compliant = premiums_paid_ytd <= policy_limit_annual
        ratio = (premiums_paid_ytd / policy_limit_annual) * 100 if policy_limit_annual > 0 else 999
        
        if not is_compliant:
            logger.error(f"COMPLIANCE_ALERT: PPLI overfunded ({ratio:.1f}%). TAX STATUS COMPROMISED.")
            
        return {
            "is_mec_compliant": is_compliant,
            "funding_ratio_pct": round(float(ratio), 2),
            "remaining_limit": round(max(Decimal('0'), policy_limit_annual - premiums_paid_ytd), 2),
            "status": "TAX_FREE_WRAPPER" if is_compliant else "TAXABLE_MEC"
        }
