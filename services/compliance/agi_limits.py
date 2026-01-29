"""
AGI Deduction Monitor.
Tracks IRS limits for charitable giving.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AGILimitMonitor:
    """Enforces donation caps relative to AGI."""
    
    STOCK_CAP = 0.30 # 30% of AGI
    CASH_CAP = 0.60 # 60% of AGI
    
    def check_deduction_room(self, agi: float, donated_cash: float, donated_stock: float) -> Dict[str, Any]:
        cash_room = (agi * self.CASH_CAP) - donated_cash
        stock_room = (agi * self.STOCK_CAP) - donated_stock
        
        return {
            "agi": agi,
            "cash_room_remaining": max(0, cash_room),
            "stock_room_remaining": max(0, stock_room)
        }
