import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class UpsideVolatilityDetector:
    """Flags if a Sharpe Ratio is unfairly lowered by frequent high positive returns."""
    
    def analyze_flaw_impact(self, returns: List[float]) -> Dict[str, Any]:
        upside = [r for r in returns if r > 0]
        downside = [r for r in returns if r < 0]
        
        up_std = np.std(upside) if len(upside) > 1 else 0
        down_std = np.std(downside) if len(downside) > 1 else 0
        
        is_penalized = up_std > down_std * 1.5
        
        if is_penalized:
            logger.warning("QUANT_LOG: Sharpe Ratio penalized by high upside volatility. Consider Sortino.")
            
        return {
            "is_artificially_lowered": is_penalized,
            "upside_vol": round(float(up_std), 4),
            "downside_vol": round(float(down_std), 4),
            "recommendation": "USE_SORTINO" if is_penalized else "USE_SHARPE"
        }
