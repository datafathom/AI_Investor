"""
Consumer Confidence Sentiment Monitor.
Ingests UMich and Conference Board indexes.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConsumerConfMonitor:
    """Monitors consumer sentiment trends."""
    
    def check_umich_index(self, score: float, prev_score: float) -> str:
        if score < 60:
             return "REMISSION_LEVELS"
        elif score < prev_score - 5:
             return "SENTIMENT_PLUNGE"
        return "OPTIMISTIC"
