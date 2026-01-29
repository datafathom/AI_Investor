"""
Lifestyle Creep Monitor.
Detects expense rising that pushes back FI dates.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LifestyleCreepMonitor:
    """Monitors spending trends against FI goals."""
    
    def check_creep(self, current_monthly: float, baseline_monthly: float) -> Dict[str, Any]:
        increase = current_monthly - baseline_monthly
        if increase <= 0: return {"creep_detected": False}
        
        # Every $1 growth in monthly expense requires $300 growth in FIRE number (25x * 12)
        added_fire_needed = increase * 300
        
        return {
            "creep_detected": True,
            "monthly_increase": increase,
            "net_worth_penalty": added_fire_needed,
            "retirement_delay_months": int(added_fire_needed / 5000) # Est monthly saving
        }
