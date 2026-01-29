"""
Macro Regime Detection Algorithm.
Detects long-term shifts in inflation and rates.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RegimeDetector:
    """Detects macro volatility regimes."""
    
    def detect_regime(self, cpi_roc: float, rate_10y_roc: float) -> str:
        if cpi_roc > 0.05 and rate_10y_roc > 0:
             return "INFLATIONARY_EXPANSION"
        elif cpi_roc < 0.02 and rate_10y_roc < 0:
             return "DEFLATIONARY_STAGNATION"
        return "NEUTRAL_GROWTH"
