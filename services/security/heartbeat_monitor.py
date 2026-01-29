"""
Dead Man's Switch Heartbeat - Phase 83.
Monitors user activity for succession.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HeartbeatMonitor:
    """Monitors user heartbeat for dead man's switch."""
    
    def __init__(self, alert_after_days: int = 30):
        self.last_heartbeat = datetime.now()
        self.alert_days = alert_after_days
    
    def ping(self):
        self.last_heartbeat = datetime.now()
    
    def get_status(self) -> Dict[str, Any]:
        days_since = (datetime.now() - self.last_heartbeat).days
        return {
            "last_activity": self.last_heartbeat.isoformat(),
            "days_inactive": days_since,
            "alert_triggered": days_since >= self.alert_days,
            "succession_pending": days_since >= self.alert_days * 2
        }
