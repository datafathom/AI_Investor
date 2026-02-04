import logging
from typing import Optional
from datetime import timezone, datetime, timedelta

logger = logging.getLogger(__name__)

class WashSaleGuardService:
    """
    Prevents Wash-Sale violations by tracking 30-day buy/sell windows.
    IRS Rule: Cannot claim loss if you buy substantially identical security 
    within 30 days before or after the sale.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WashSaleGuardService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.wash_window_days = 30
        logger.info("WashSaleGuardService initialized")

    def is_safe_to_harvest(
        self, 
        symbol: str, 
        last_purchase_date: Optional[datetime] = None
    ) -> bool:
        """
        Check if it's safe to harvest a loss without triggering wash-sale.
        """
        if last_purchase_date is None:
            return True
            
        days_since_purchase = (datetime.now(timezone.utc) - last_purchase_date).days
        
        if days_since_purchase <= self.wash_window_days:
            logger.warning(f"WASH-SALE RISK: {symbol} purchased {days_since_purchase} days ago")
            return False
            
        return True

    def is_safe_to_repurchase(
        self, 
        symbol: str, 
        last_sale_date: Optional[datetime] = None
    ) -> bool:
        """
        Check if it's safe to repurchase after a loss harvest.
        """
        if last_sale_date is None:
            return True
            
        days_since_sale = (datetime.now(timezone.utc) - last_sale_date).days
        
        if days_since_sale <= self.wash_window_days:
            logger.warning(f"WASH-SALE RISK: {symbol} sold {days_since_sale} days ago")
            return False
            
        return True

    def get_safe_repurchase_date(self, sale_date: datetime) -> datetime:
        """Calculate the earliest safe repurchase date."""
        return sale_date + timedelta(days=self.wash_window_days + 1)
