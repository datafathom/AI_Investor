"""
Macro Regime Classifier - Phase 35.
Classifies market into macro regimes for strategy selection.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RegimeClassifier:
    """Classifies current market regime."""
    
    @staticmethod
    def classify(vix: float, trend_strength: float, correlation: float) -> str:
        if vix > 30:
            return "CRISIS"
        elif vix > 20:
            return "HIGH_VOL"
        elif trend_strength > 0.7:
            return "TRENDING"
        elif trend_strength < 0.3:
            return "RANGING"
        return "NORMAL"
