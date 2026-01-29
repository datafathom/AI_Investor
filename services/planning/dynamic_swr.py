"""
Dynamic Withdrawal Rate (CAPE-Based).
Adjusts SWR based on market valuations to prevent failure.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DynamicSWR:
    """Adjusts withdrawal % based on current Shiller PE (CAPE)."""
    
    def get_safe_withdrawal_rate(self, current_cape: float) -> float:
        if current_cape > 35: return 0.03 # 3% for overvalued
        elif current_cape < 15: return 0.05 # 5% for undervalued
        return 0.04 # Standard 4%
