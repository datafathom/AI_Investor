import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class FREDStreamService:
    """
    Ingests Federal Reserve Economic Data (FRED) for macro analysis.
    Publishes to Kafka topic `macro-fred-updates`.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FREDStreamService, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key: Optional[str] = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.api_key = api_key
        self.kafka_topic = "macro-fred-updates"
        logger.info("FREDStreamService initialized")

    def fetch_treasury_yields(self) -> Dict[str, float]:
        """Fetch current Treasury yield curve data."""
        # Mock data - would integrate with real FRED API
        return {
            "US_1M": 5.25, "US_3M": 5.30, "US_6M": 5.20,
            "US_1Y": 4.85, "US_2Y": 4.50, "US_5Y": 4.10,
            "US_10Y": 4.05, "US_30Y": 4.25
        }

    def is_curve_inverted(self) -> bool:
        """Check if yield curve is inverted (2Y > 10Y)."""
        yields = self.fetch_treasury_yields()
        inverted = yields.get("US_2Y", 0) > yields.get("US_10Y", 0)
        if inverted:
            logger.warning("YIELD CURVE INVERTED - Recession signal")
        return inverted

    def get_fed_funds_rate(self) -> float:
        """Get current Fed Funds target rate."""
        return 5.25  # Mock

    def publish_to_kafka(self, data: Dict[str, Any]) -> bool:
        """Publish macro data to Kafka topic."""
        # Mock implementation
        logger.info(f"Published to {self.kafka_topic}: {len(data)} items")
        return True
