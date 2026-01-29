"""
Expectancy Model Service.
Calculates the system's mathematical edge using the R-Multiple framework.
Expectancy = (Win% * Average Win R) - (Loss% * Average Loss R)
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ExpectancyModel:
    """
    Evaluates the statistical probability of ongoing profitability.
    """

    @staticmethod
    def calculate_expectancy(r_multiples: List[float]) -> Dict[str, Any]:
        """
        Calculate expectancy from a sequence of closed trade R-multiples.
        """
        if not r_multiples:
            return {"expectancy": 0.0, "win_rate": 0.0, "sample_size": 0}

        wins = [r for r in r_multiples if r > 0]
        losses = [r for r in r_multiples if r <= 0]
        
        total_count = len(r_multiples)
        win_count = len(wins)
        
        win_rate = win_count / total_count
        avg_win_r = sum(wins) / win_count if win_count > 0 else 0.0
        avg_loss_r = abs(sum(losses) / (total_count - win_count)) if (total_count - win_count) > 0 else 0.0
        
        # Expectancy Formula
        # E = (Win Rate * Avg Win) - (Loss Rate * Avg Loss)
        expectancy = (win_rate * avg_win_r) - ((1 - win_rate) * avg_loss_r)
        
        return {
            "expectancy": round(expectancy, 4),
            "win_rate": round(win_rate * 100, 2),
            "avg_win_r": round(avg_win_r, 2),
            "avg_loss_r": round(avg_loss_r, 2),
            "sample_size": total_count,
            "status": "POSITIVE_EDGE" if expectancy > 0 else "NEGATIVE_EDGE"
        }
