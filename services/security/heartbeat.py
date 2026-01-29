"""
Dead Man's Switch Heartbeat.
Monitors user activity for estate trigger.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EstateHeartbeat:
    """Monitors heartbeat for succession protocol."""
    
    def __init__(self, check_in_days: int = 90):
        self.last_check_in = datetime.now()
        self.interval = timedelta(days=check_in_days)
        
    def check_in(self):
        self.last_check_in = datetime.now()
        
    def get_time_to_trigger(self) -> Dict[str, Any]:
        deadline = self.last_check_in + self.interval
        remaining = deadline - datetime.now()
        
        is_triggered = remaining.total_seconds() < 0
        
        return {
            "last_active": self.last_check_in.isoformat(),
            "trigger_deadline": deadline.isoformat(),
            "days_remaining": max(0, remaining.days),
            "is_triggered": is_triggered
        }
