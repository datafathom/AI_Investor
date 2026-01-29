"""
Baltic Dry Index (BDI) Monitor.
Tracks raw material shipping demand.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BDIMonitor:
    """Monitors raw material shipping rates."""
    
    def analyze_bdi(self, score: int, moving_avg: float) -> str:
        if score > moving_avg * 1.5:
             return "GLOBAL_DEMAND_SURGE"
        elif score < moving_avg * 0.7:
             return "TRADE_CONTRACTION"
        return "STABLE"
