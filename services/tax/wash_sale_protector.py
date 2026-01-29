"""
Wash-Sale Protection - Phase 76.
Prevents wash sale violations.
"""
import logging
from datetime import date, timedelta
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class WashSaleProtector:
    """Prevents wash sale violations."""
    
    def __init__(self):
        self.recent_sales: List[Dict[str, Any]] = []
    
    def record_sale(self, symbol: str, sale_date: date):
        self.recent_sales.append({"symbol": symbol, "date": sale_date})
    
    def can_buy(self, symbol: str, buy_date: date) -> bool:
        for sale in self.recent_sales:
            if sale["symbol"] == symbol:
                days_diff = (buy_date - sale["date"]).days
                if -30 <= days_diff <= 30:
                    return False
        return True
