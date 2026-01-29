"""
Retail BS Noise Filter - Phase 28.
Filters out low-quality retail-style signals.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NoiseFilter:
    """Filters retail-quality signals."""
    
    @staticmethod
    def is_valid_signal(signal: Dict[str, Any]) -> bool:
        # Reject signals based on common retail patterns
        if signal.get("source") == "RETAIL_INDICATOR":
            return False
        if signal.get("confluence_count", 0) < 3:
            return False
        return True
