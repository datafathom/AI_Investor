import logging
from datetime import date
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CitizenshipHedgingService:
    """
    Manages 'Plan B' citizenship mobility and tax residency tracking.
    Tracks 183-day rules and Golden Visa investment compliance.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CitizenshipHedgingService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("CitizenshipHedgingService initialized")

    def track_residency_threshold(self, country_code: str, days_present: int) -> Dict[str, Any]:
        """
        Policy: Stay < 183 days to avoid becoming an accidental tax resident.
        """
        limit = 183
        cushion = limit - days_present
        
        return {
            "country": country_code,
            "days_spent": days_present,
            "days_remaining_to_resident": cushion,
            "status": "SAFE" if cushion > 30 else "RISK_OF_TAX_RECOGNITION"
        }

    def validate_visa_investment_hold(self, purchase_date: date, required_years: int = 5) -> Dict[str, Any]:
        """
        Policy: Golden Visa assets must be held for X years.
        """
        today = date.today()
        years_held = (today.year - purchase_date.year) - ((today.month, today.day) < (purchase_date.month, purchase_date.day))
        is_vested = years_held >= required_years
        
        return {
            "years_held": years_held,
            "is_eligible_for_citizenship": is_vested,
            "vesting_progress_pct": round((years_held / required_years) * 100, 2) if required_years > 0 else 100
        }
