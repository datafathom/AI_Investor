import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ToxicityMonitor:
    """
    Measures Order Flow Toxicity (VPIN) to detect impending liquidity crashes.
    High toxicity implies informed sellers are overwhelming market makers.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ToxicityMonitor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("ToxicityMonitor initialized")

    def calculate_vpin_status(self, buy_volume: int, sell_volume: int, avg_vpin: float) -> Dict[str, Any]:
        """
        Simplified VPIN: |Buy - Sell| / (Buy + Sell).
        """
        total = buy_volume + sell_volume
        if total == 0:
            return {"vpin": 0, "status": "NO_VOLUME"}
            
        imbalance = abs(buy_volume - sell_volume)
        current_vpin = imbalance / total
        
        is_toxic = current_vpin > (avg_vpin * 2.0)
        
        return {
            "vpin_score": round(current_vpin, 4),
            "toxicity_alert": is_toxic,
            "liquidity_risk": "CRITICAL" if is_toxic else "STABLE"
        }
