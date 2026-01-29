import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SequenceRiskCalculator:
    """Calculates Sequence of Returns Risk (SORR) impact in early retirement."""
    
    def analyze_sorr(self, initial_withdrawal_rate: float, first_3y_returns: list[float]) -> Dict[str, Any]:
        """
        Identifies high risk if negative returns occur while withdrawing at >4%.
        """
        negative_years = [r for r in first_3y_returns if r < 0]
        avg_ret = sum(first_3y_returns) / len(first_3y_returns) if first_3y_returns else 0
        
        is_high_risk = avg_ret < 0 and initial_withdrawal_rate >= 0.04
        
        if is_high_risk:
            logger.warning(f"RET_ALERT: High Sequence Risk! Negative returns during drawdown. Avg: {avg_ret:.2%}")
            
        return {
            "is_sorr_triggered": is_high_risk,
            "avg_early_return": round(avg_ret, 4),
            "negative_count": len(negative_years),
            "recommendation": "REDUCE_WITHDRAWAL" if is_high_risk else "CONTINUE_NORMAL"
        }
