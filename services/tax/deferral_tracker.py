import logging
from datetime import date
from typing import List, Dict, Any
from models.private_banking_client import TaxDeferralStrategy

logger = logging.getLogger(__name__)

class DeferralTracker:
    """Tracks and calculates remaining time for tax deferral strategies."""
    
    def calculate_days_remaining(self, strategy: TaxDeferralStrategy) -> int:
        if not strategy.expiration_date: return 9999
        delta = strategy.expiration_date - date.today()
        days = max(0, delta.days)
        
        if days < 30:
            logger.warning(f"DEFERRAL_ALERT: Strategy {strategy.id} expires in {days} days!")
            
        return days

    def estimate_tax_savings(self, deferred_gain: float, tax_rate: float) -> float:
        return deferred_gain * tax_rate
