"""
High Conviction Insider Alert.
Filters for significant ($>500k) insider purchases.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HighConvictionFilter:
    """Filters for high-conviction signals."""
    
    CONVICTION_THRESHOLD = 500000.0 # $500k
    
    def is_high_conviction(self, total_value: float) -> bool:
        return total_value >= self.CONVICTION_THRESHOLD
