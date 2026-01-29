"""
Volatility Targeting Engine.
Dynamically de-leverages during market spikes.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VolTargeting:
    """Enforces constant risk via leverage adjustment."""
    
    TARGET_VOL = 0.15 # 15% annual vol target
    
    def calculate_leverage(self, current_vol: float) -> float:
        if current_vol <= 0: return 1.0
        
        lev = self.TARGET_VOL / current_vol
        # Cap at 2.0 (Ayres/Nalebuff limit)
        return min(2.0, round(lev, 2))
