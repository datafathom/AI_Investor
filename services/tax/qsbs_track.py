"""
QSBS Eligibility Tracker.
Tracks holding periods for section 1202 tax exclusion.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class QSBSTracker:
    """Manages QSBS tax qualification."""
    
    def check_eligibility(self, acquisition_date: str, gross_assets_at_issuance: float) -> Dict[str, Any]:
        acquired = datetime.fromisoformat(acquisition_date)
        holding_years = (datetime.now() - acquired).days / 365.25
        
        is_qualified = gross_assets_at_issuance < 50000000.0 # $50M limit
        can_exclude = holding_years >= 5.0
        
        return {
            "is_qsbs_certified": is_qualified,
            "years_held": round(holding_years, 2),
            "fully_excludable": is_qualified and can_exclude,
            "status": "ELGIBLE_IN_FUTURE" if is_qualified and not can_exclude else "QUALIFIED" if can_exclude else "NOT_QSBS"
        }
