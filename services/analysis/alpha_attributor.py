"""
Alpha Attributor Service.
Differentiates between consistent edge and outlier luck.
Calculates 'Adjusted Expectancy' by capping extreme winner R-multiples.
"""
import logging
from typing import List, Dict, Any
from services.analysis.expectancy_engine import ExpectancyEngine

logger = logging.getLogger(__name__)

class AlphaAttributor:
    """
    Quality control for strategy performance.
    """

    @staticmethod
    def calculate_adjusted_expectancy(r_multiples: List[float], outlier_cap: float = 10.0) -> Dict[str, Any]:
        """
        Calculate expectancy while capping outlier trades to see base skill.
        
        :param r_multiples: List of trade R-multiples
        :param outlier_cap: Max R allowed in the adjusted calculation (e.g., 10R)
        """
        if not r_multiples:
            return {"adjusted_expectancy": 0.0, "outliers_detected": 0}

        adjusted_rs = [min(r, outlier_cap) if r > 0 else r for r in r_multiples]
        
        wins = [r for r in adjusted_rs if r > 0]
        losses = [r for r in adjusted_rs if r <= 0]
        
        win_rate = len(wins) / len(r_multiples)
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0.0
        
        adj_expectancy = ExpectancyEngine.calculate_expectancy(win_rate, avg_win, avg_loss)
        
        outliers = [r for r in r_multiples if r > outlier_cap]
        
        return {
            "base_expectancy": adj_expectancy,
            "outliers_found": len(outliers),
            "outlier_rs": outliers,
            "quality_tier": "INSTITUTIONAL" if adj_expectancy > 0.3 else "VULNERABLE"
        }
