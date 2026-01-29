import logging
from datetime import date
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RecoveryTracker:
    """Tracks drawdown recovery timelines and trough identification."""
    
    def analyze_recovery(self, current_value: float, peak_value: float, peak_date: date) -> Dict[str, Any]:
        """
        Determines how far a portfolio is from its previous high.
        """
        drawdown = 0.0
        is_in_recovery = current_value < peak_value
        
        if is_in_recovery:
            drawdown = (peak_value - current_value) / peak_value
            
        logger.info(f"PERF_LOG: Drawdown status: {drawdown:.2%} off peak of ${peak_value:,.2f}")
        
        return {
            "is_under_peak": is_in_recovery,
            "drawdown_pct": round(drawdown, 4),
            "days_since_peak": (date.today() - peak_date).days if is_in_recovery else 0
        }
