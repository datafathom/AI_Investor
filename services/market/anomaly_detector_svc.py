import logging
import numpy as np
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AnomalyDetectorService:
    """
    Detects market manipulation signatures in price and volume data.
    Specifically targets 'Pump and Dump' patterns where price rises on declining or fake volume.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AnomalyDetectorService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("AnomalyDetectorService initialized")

    def detect_price_volume_divergence(
        self, 
        price_series: List[float], 
        volume_series: List[float], 
        ticker: str
    ) -> Dict[str, Any]:
        """
        Policy: Price UP + Volume DOWN = Divergence (Warning).
        Price UP + Volume UP = Confirmation (Safe).
        """
        if len(price_series) != len(volume_series) or len(price_series) < 5:
            return {"status": "INSUFFICIENT_DATA"}

        # Calculate trends
        price_change = (price_series[-1] - price_series[0]) / price_series[0]
        
        # Volume trend: Split into first half vs second half
        mid_point = len(volume_series) // 2
        vol_early = sum(volume_series[:mid_point]) / mid_point
        # Ensure we don't divide by zero if list is empty (though length check handles it)
        len_late = len(volume_series) - mid_point
        vol_late = sum(volume_series[mid_point:]) / len_late
        
        vol_change = (vol_late - vol_early) / vol_early if vol_early > 0 else 0

        # Divergence Logic
        divergence_score = 0
        anomaly_type = "NONE"
        
        if price_change > 0.10 and vol_change < -0.10:
            # Dangerous: Price up 10%, Volume down 10%
            divergence_score = 85
            anomaly_type = "PRICE_VOL_DIVERGENCE_PUMP"
        elif price_change < -0.10 and vol_change > 0.50:
            # Panic selling: Price down, Volume massive
            divergence_score = 60
            anomaly_type = "PANIC_DUMP"

        risk_level = "CRITICAL" if divergence_score > 80 else "MEDIUM" if divergence_score > 50 else "LOW"

        if divergence_score > 50:
            logger.warning(f"INTEGRITY_ALERT: {ticker} shows {anomaly_type}. Score: {divergence_score}")

        return {
            "ticker": ticker,
            "price_trend_pct": round(price_change * 100, 2),
            "volume_trend_pct": round(vol_change * 100, 2),
            "divergence_score": divergence_score,
            "anomaly_type": anomaly_type,
            "risk_level": risk_level
        }
