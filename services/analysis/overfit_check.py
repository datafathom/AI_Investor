"""
Overfitting Variance Matrix.
Detects over-optimized strategies.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OverfitChecker:
    """Checks for strategy overfitting."""
    
    def check_variance(self, is_sharpe: float, oos_sharpe: float) -> Dict[str, Any]:
        """Compare In-Sample vs Out-of-Sample Sharpe ratios."""
        if is_sharpe == 0:
            return {"overfit": False, "variance": 0}
            
        variance = (is_sharpe - oos_sharpe) / is_sharpe
        
        # If OOS is significantly worse, it's likely overfit
        is_overfit = variance > 0.20
        
        return {
            "variance_pct": round(variance * 100, 2),
            "is_overfit": is_overfit,
            "status": "DANGER" if is_overfit else "ROBUST"
        }
