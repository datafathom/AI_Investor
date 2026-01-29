import logging
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LifestyleBurnService:
    """
    Projects lifestyle costs forward into the future using the CLEW rate.
    Determines the "Required Corpus" to maintain standard of living indefinitely.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LifestyleBurnService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("LifestyleBurnService initialized")

    def project_burn_rate(self, current_annual_spend: Decimal, clew_rate: Decimal, years: int = 30) -> Dict[str, Any]:
        """
        Policy: Future Cost = Present Cost * (1 + CLEW)^Years.
        """
        future_burn = current_annual_spend * ((1 + clew_rate) ** years)
        
        # Sustainable Withdrawal Rate (SWR) usually 3% for UHNW capital preservation
        required_corpus_future = future_burn / Decimal('0.03')
        
        return {
            "years_projected": years,
            "current_spend": round(current_annual_spend, 2),
            "future_spend_annual": round(future_burn, 2),
            "clew_rate_used": round(clew_rate, 4),
            "required_corpus_at_future_date": round(required_corpus_future, 2)
        }
