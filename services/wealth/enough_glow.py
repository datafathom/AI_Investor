"""
Zen Mode: The 'Enough' Metric Glow - Phase 90.
Visual indicator of financial independence.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EnoughGlow:
    """Visual indicator for 'enough' achievement."""
    
    LEVELS = {
        0: {"color": "RED", "message": "Building Foundation"},
        25: {"color": "ORANGE", "message": "Making Progress"},
        50: {"color": "YELLOW", "message": "Halfway There"},
        75: {"color": "LIGHT_GREEN", "message": "Almost There"},
        100: {"color": "GOLD", "message": "Financial Independence Achieved"}
    }
    
    @staticmethod
    def get_glow(progress_pct: float) -> Dict[str, Any]:
        for threshold in sorted(EnoughGlow.LEVELS.keys(), reverse=True):
            if progress_pct >= threshold:
                return EnoughGlow.LEVELS[threshold]
        return EnoughGlow.LEVELS[0]
