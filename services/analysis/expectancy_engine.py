"""
Expectancy Engine Service.
Calculates the system's mathematical edge using combined RR and WinRate data.
Expectancy = (Win% * Avg Win R) - (Loss% * Avg Loss R)
"""
import logging
from typing import List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class ExpectancyEngine:
    """
    Core mathematical model for confirming a sustainable trading edge.
    """

    @staticmethod
    def calculate_expectancy(win_rate: float, avg_win_r: float, avg_loss_r: float) -> float:
        """
        Calculate mathematical expectancy for a given dataset.
        
        :param win_rate: Percentage of winning trades (0.0 to 1.0)
        :param avg_win_r: Average R-multiple of winning trades
        :param avg_loss_r: Average R-multiple of losing trades (absolute value)
        :return: float expectancy (Net R per trade)
        """
        loss_rate = 1.0 - win_rate
        expectancy = (win_rate * avg_win_r) - (loss_rate * abs(avg_loss_r))
        return round(float(expectancy), 4)

    @staticmethod
    def identify_superior_strategy(strat_a: Dict[str, Any], strat_b: Dict[str, Any]) -> str:
        """
        Compare two strategies based on expectancy.
        """
        exp_a = ExpectancyEngine.calculate_expectancy(strat_a['win_rate'], strat_a['avg_win_r'], strat_a['avg_loss_r'])
        exp_b = ExpectancyEngine.calculate_expectancy(strat_b['win_rate'], strat_b['avg_win_r'], strat_b['avg_loss_r'])
        
        if exp_a > exp_b:
            return strat_a.get('name', 'Strategy A')
        else:
            return strat_b.get('name', 'Strategy B')
