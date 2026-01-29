import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VolatilityCalculator:
    """Calculates risk metrics: StdDev, Downside Dev, Max Drawdown."""
    
    def calculate_annualized_vol(self, returns: List[float]) -> float:
        if not returns: return 0.0
        # Standard deviation of returns * sqrt(252)
        std = np.std(returns)
        ann_vol = std * np.sqrt(252)
        return round(float(ann_vol), 4)

    def calculate_var_95(self, returns: List[float], initial_investment: float = 100000) -> float:
        """Parametric VaR at 95% Confidence."""
        if not returns: return 0.0
        avg_ret = np.mean(returns)
        std_ret = np.std(returns)
        # 1.645 for 95%
        var_pct = 1.645 * std_ret - avg_ret
        return round(var_pct * initial_investment, 2)

    def calculate_max_drawdown(self, equity_curve: List[float]) -> float:
        if not equity_curve: return 0.0
        peak = equity_curve[0]
        max_dd = 0
        for val in equity_curve:
            if val > peak: peak = val
            dd = (peak - val) / peak
            if dd > max_dd: max_dd = dd
        return round(float(max_dd), 4)
