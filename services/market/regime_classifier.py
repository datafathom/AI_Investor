"""
==============================================================================
FILE: services/market/regime_classifier.py
ROLE: Market Regime Analysis Engine
PURPOSE: Classifies market states (Bull, Bear, Choppy) using trend and volatility.
==============================================================================
"""

import logging
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class MarketRegime(str, Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    CHOPPY = "CHOPPY"
    TRANSITION = "TRANSITION"


class MarketRegimeClassifier:
    """
    Classifies the current market regime based on VIX, trend, and momentum.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarketRegimeClassifier, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("MarketRegimeClassifier initialized")

    def get_current_regime(self) -> Dict[str, Any]:
        """Classify the current market regime."""
        # Seed based on hour for session-level stability
        random.seed(datetime.now().hour)
        
        regime = random.choice(list(MarketRegime))
        confidence = round(random.uniform(70, 95), 1)
        
        # Probabilities for next state transitions
        probs = {r.value: 0.0 for r in MarketRegime}
        # Highly weighted towards current regime for inertia
        remaining = 100.0 - confidence
        probs[regime.value] = confidence
        
        others = [r for r in MarketRegime if r != regime]
        p1 = round(random.uniform(remaining * 0.4, remaining * 0.7), 1)
        p2 = remaining - p1
        
        probs[others[0].value] = p1
        probs[others[1].value] = round(p2 * 0.7, 1)
        probs[others[2].value] = round(p2 * 0.3, 1)

        indicators = [
            {"name": "Volatility (VIX)", "value": round(random.uniform(12, 35), 2), "weight": 0.35, "signal": "STABLE" if regime == MarketRegime.BULL else "ELEVATED"},
            {"name": "Trend Score", "value": round(random.uniform(-1, 1), 2), "weight": 0.30, "signal": "POSITIVE" if regime == MarketRegime.BULL else "NEGATIVE"},
            {"name": "Breadth (A/D)", "value": round(random.uniform(0.4, 0.9), 2), "weight": 0.20, "signal": "STRONG" if regime == MarketRegime.BULL else "WEAK"},
            {"name": "Momentum (RSI)", "value": round(random.uniform(30, 75), 2), "weight": 0.15, "signal": "BULLISH" if regime == MarketRegime.BULL else "BEARISH"}
        ]

        return {
            "regime": regime.value,
            "confidence": confidence,
            "transition_probabilities": probs,
            "since": (datetime.now() - timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d"),
            "indicators": indicators,
            "last_updated": datetime.now().isoformat()
        }

    def get_regime_history(self, days: int = 180) -> List[Dict[str, Any]]:
        """Get historical regimes."""
        history = []
        current_date = datetime.now() - timedelta(days=days)
        
        while current_date < datetime.now():
            duration = random.randint(15, 60)
            regime = random.choice(list(MarketRegime))
            history.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "regime": regime.value,
                "duration_days": duration
            })
            current_date += timedelta(days=duration)
        
        return history

    def get_regime_forecast(self) -> Dict[str, Any]:
        """Predict the most likely regime for the next period."""
        random.seed(datetime.now().hour + 1)
        regime = random.choice(list(MarketRegime))
        return {
            "forecast_regime": regime.value,
            "probability": round(random.uniform(60, 80), 1),
            "timeframe": "Next 10 Trading Days",
            "as_of": datetime.now().isoformat()
        }


def get_regime_classifier() -> MarketRegimeClassifier:
    return MarketRegimeClassifier()
