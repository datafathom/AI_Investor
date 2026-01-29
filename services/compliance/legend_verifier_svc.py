import logging
from datetime import date, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LegendVerifierService:
    """
    Manages the removal of 'Restricted Legends' from Rule 144(a) securities.
    Ensures 'Safe Harbor' compliance before any sale is attempted.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LegendVerifierService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("LegendVerifierService initialized")

    def check_legend_removal_eligibility(
        self, 
        acquisition_date: date, 
        is_reporting_company: bool
    ) -> Dict[str, Any]:
        """
        Policy: 
        - Reporting Companies (public > 90 days): 6 month hold.
        - Non-Reporting Companies: 1 year hold.
        """
        required_months = 6 if is_reporting_company else 12
        # Approx days
        required_days = required_months * 30 
        
        today = date.today()
        elapsed_days = (today - acquisition_date).days
        
        is_eligible = elapsed_days >= required_days
        eligible_date = acquisition_date + timedelta(days=required_days)
        
        status = "LEGEND_REMOVABLE" if is_eligible else "RESTRICTED"
        
        logger.info(f"COMPLIANCE_LOG: 144(a) Check. Held {elapsed_days} days. Eligible? {is_eligible}")
        
        return {
            "acquisition_date": acquisition_date.isoformat(),
            "issuer_type": "REPORTING" if is_reporting_company else "NON_REPORTING",
            "required_holding_period_months": required_months,
            "is_eligible_for_removal": is_eligible,
            "earliest_sale_date": eligible_date.isoformat(),
            "status": status
        }
