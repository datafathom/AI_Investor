"""
Behavioral Log Service.
Journals emotional events and prevented trades.
"""
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class BehavioralLog:
    """Logs behavioral events."""
    
    def __init__(self):
        self.logs = []
        
    def log_event(self, event_type: str, details: str, sentiment_score: int = 0):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
            "sentiment_score": sentiment_score
        }
        self.logs.append(entry)
        logger.info(f"BEHAVIORAL_LOG: [{event_type}] {details}")
        
    def get_recent_logs(self, limit: int = 10) -> list:
        return self.logs[-limit:]
