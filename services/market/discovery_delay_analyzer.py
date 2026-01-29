import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DiscoveryDelayAnalyzer:
    """Analyzes time delays in price adjustment after market events."""
    
    def calculate_delay_score(self, event_type: str, seconds: int, passive_pct: float) -> float:
        """
        Higher score means more delay is attributed to passive/automated trading.
        """
        base_delay = 0.5
        # Passive dominance over 60% starts increasing delay score
        passive_factor = max(0, (passive_pct - 0.6) * 2)
        
        score = base_delay + (seconds / 100) + passive_factor
        
        logger.info(f"DISCOVERY_LOG: Event {event_type} had {seconds}s delay. Score: {score:.2f}")
        return round(score, 4)
