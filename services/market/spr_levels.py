"""
SPR Level Tracker.
Monitors US Strategic Petroleum Reserve inventory.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SPRTracker:
    """Tracks oil reserve levels."""
    
    def check_reserves(self, current_mbbl: float, historical_avg: float) -> str:
        pct_of_avg = current_mbbl / historical_avg
        if pct_of_avg < 0.6:
             logger.critical(f"ENERGY_DANGER: SPR reserves at {pct_of_avg*100:.1f}% of historical average. US vulnerable to supply shocks.")
             return "CRITICAL_LOW"
        return "ADEQUATE"
