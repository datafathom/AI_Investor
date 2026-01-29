"""
The 'Enough' Zen Mode GUI - Phase 80.
Achievement tracking for financial independence.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EnoughCalculator:
    """Calculates 'Enough' achievement."""
    
    def __init__(self, monthly_expenses: float, years_to_cover: int = 30):
        self.monthly = monthly_expenses
        self.years = years_to_cover
    
    def get_target(self, withdrawal_rate: float = 0.04) -> float:
        annual_need = self.monthly * 12
        return annual_need / withdrawal_rate
    
    def get_progress(self, current_net_worth: float) -> Dict[str, Any]:
        target = self.get_target()
        pct = (current_net_worth / target) * 100
        
        return {
            "target": target,
            "current": current_net_worth,
            "progress_pct": min(pct, 100),
            "achieved": pct >= 100,
            "remaining": max(0, target - current_net_worth)
        }
