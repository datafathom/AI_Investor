import logging
from datetime import date

logger = logging.getLogger(__name__)

class ProrationService:
    """Calculates fee proration for partial billing periods."""
    
    def calculate_proration_factor(self, start_date: date, end_date: date, period_days: int = 90) -> float:
        """
        Calculates how much of a billing period was 'active'.
        """
        days_active = (end_date - start_date).days + 1
        factor = days_active / period_days
        
        logger.info(f"BILLING_LOG: Proration factor: {factor:.4f} ({days_active} days active)")
        return round(min(1.0, factor), 6)
