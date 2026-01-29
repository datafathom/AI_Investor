"""
Emergency Moat Service.
Tracks emergency fund health.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EmergencyMoat:
    """Tracks emergency fund status."""
    
    def __init__(self, monthly_expenses: float):
        self.monthly_expenses = monthly_expenses
        
    def check_health(self, current_balance: float) -> Dict[str, Any]:
        months_covered = current_balance / self.monthly_expenses if self.monthly_expenses > 0 else 0
        
        status = "CRITICAL"
        if months_covered >= 6: status = "HEALTHY"
        elif months_covered >= 3: status = "ADEQUATE"
        elif months_covered >= 1: status = "WARNING"
        
        return {
            "months_covered": round(months_covered, 1),
            "status": status,
            "target_6_months": self.monthly_expenses * 6
        }
