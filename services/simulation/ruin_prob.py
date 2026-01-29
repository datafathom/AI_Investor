"""
Probability of Ruin Calculator.
Calculates risk of blowout in backtests.
"""
import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RuinCalculator:
    """Calculates ruin probability using path outcomes."""
    
    RUIN_THRESHOLD = -0.50 # 50% drawdown
    
    def calculate_ruin_prob(self, equity_paths: np.ndarray) -> Dict[str, Any]:
        """
        equity_paths: 2D array (n_sims, n_steps) of returns or equity curves.
        """
        n_sims = equity_paths.shape[0]
        
        # Check if any path hits the threshold
        min_equity = np.min(equity_paths, axis=1)
        ruined_count = np.sum(min_equity <= self.RUIN_THRESHOLD)
        
        prob = ruined_count / n_sims
        
        return {
            "ruin_probability": prob,
            "status": "PASS" if prob < 0.001 else "FAIL",
            "fail_reason": "High risk of bankruptcy detected" if prob >= 0.001 else None
        }
