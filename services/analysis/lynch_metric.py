"""
Peter Lynch Legend Metric.
metric calculator for 60% win rate baseline.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LynchMetric:
    """Calculates deviation from Peter Lynch theoretical baseline."""
    
    BASELINE_WIN_RATE = 0.60
    BASELINE_RR = 2.0
    
    @staticmethod
    def calculate_deviation(win_rate: float, avg_rr: float) -> Dict[str, Any]:
        win_dev = win_rate - LynchMetric.BASELINE_WIN_RATE
        rr_dev = avg_rr - LynchMetric.BASELINE_RR
        
        status = "LEGEND" if win_rate >= 0.6 and avg_rr >= 2.0 else "DEVELOPING"
        
        return {
            "win_rate_deviation": round(win_dev, 4),
            "rr_deviation": round(rr_dev, 4),
            "lynch_status": status
        }
