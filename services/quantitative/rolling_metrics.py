import logging
import numpy as np
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RollingMetricsEngine:
    """Calculates windowed risk-adjusted performance metrics."""
    
    def calculate_rolling_sharpe(self, returns: List[float], rf_rate: float, window: int = 252*3) -> List[float]:
        """
        Policy: Annualized Sharpe over rolling 3-year window (252*3 trading days).
        Formula: (MeanReturn - Rf) / StdDev
        """
        if len(returns) < window: return []
        
        results = []
        for i in range(len(returns) - window + 1):
            subset = returns[i : i + window]
            avg_ret = np.mean(subset) * 252
            std_dev = np.std(subset) * np.sqrt(252)
            
            sharpe = (avg_ret - rf_rate) / std_dev if std_dev > 0 else 0
            results.append(round(float(sharpe), 4))
            
        logger.info(f"QUANT_LOG: Calculated {len(results)} rolling Sharpe points (Window: {window})")
        return results

    def calculate_sortino(self, returns: List[float], rf_rate: float, target_return: float = 0.0) -> float:
        """Isolated Sortino for a single window."""
        avg_ret = np.mean(returns) * 252
        downside_returns = [r for r in returns if r < target_return]
        downside_std = np.std(downside_returns) * np.sqrt(252) if downside_returns else 0.0001
        
        sortino = (avg_ret - rf_rate) / downside_std
        return round(float(sortino), 4)
