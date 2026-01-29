import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FATCAComplianceService:
    """
    Automates FATCA and FBAR reporting requirements for foreign financial assets.
    Tracks Max Value During Year (FBAR) and Year-End Value (8938/FATCA).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FATCAComplianceService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("FATCAComplianceService initialized")

    def check_reporting_thresholds(self, total_foreign_value: Decimal, is_us_resident: bool = True) -> Dict[str, Any]:
        """
        Policy: 
        FBAR (FinCEN 114): >$10k at any time.
        FATCA (Form 8938): >$50k end of year (Single, Resident).
        """
        requires_fbar = total_foreign_value > Decimal('10000')
        requires_fatca = total_foreign_value > Decimal('50000')
        
        if requires_fbar:
            logger.warning(f"COMPLIANCE_ALERT: FBAR Filing Required. Account value ${total_foreign_value:,.2f} > $10k.")
            
        return {
            "total_foreign_value": round(total_foreign_value, 2),
            "requires_fbar_filing": requires_fbar,
            "requires_8938_filing": requires_fatca,
            "penalty_risk": "CRITICAL" if total_foreign_value > Decimal('100000') and not requires_fbar else "LOW"
        }
