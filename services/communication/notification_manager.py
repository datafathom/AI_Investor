"""
==============================================================================
FILE: services/communication/notification_manager.py
ROLE: Alert Router
PURPOSE:
    Handle delivery of system messages to user channels (SMS, Email, Push).
    
    1. Channel Routing:
       - CRITICAL -> SMS + Push + Email
       - WARNING -> Push + Email
       - INFO -> Log/Dashboard only
       
    2. Mock Implementation:
       - Prints to console/log instead of actual API calls for now.
       
ROADMAP: Phase 29 - User Personalization
==============================================================================
"""

import logging
from enum import Enum
from typing import List, Dict

logger = logging.getLogger(__name__)

class AlertPriority(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class NotificationChannel(Enum):
    CONSOLE = "CONSOLE"
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"

class NotificationManager:
    def __init__(self):
        self.history: List[Dict] = []
        
    def send_alert(self, message: str, priority: AlertPriority = AlertPriority.INFO):
        """
        Route alert to appropriate channels based on priority.
        """
        channels = self._get_channels_for_priority(priority)
        
        record = {
            "message": message,
            "priority": priority.value,
            "channels": [c.value for c in channels],
            "timestamp": "now" # In real app, use datetime
        }
        self.history.append(record)
        
        for channel in channels:
            self._deliver(channel, message)
            
    def _get_channels_for_priority(self, priority: AlertPriority) -> List[NotificationChannel]:
        if priority == AlertPriority.CRITICAL:
            return [NotificationChannel.SMS, NotificationChannel.PUSH, NotificationChannel.EMAIL, NotificationChannel.CONSOLE]
        elif priority == AlertPriority.WARNING:
            return [NotificationChannel.PUSH, NotificationChannel.EMAIL, NotificationChannel.CONSOLE]
        else:
            return [NotificationChannel.CONSOLE]
            
    def _deliver(self, channel: NotificationChannel, message: str):
        """
        Mock delivery to channel.
        """
        prefix = f"[{channel.value}]"
        logger.info(f"{prefix} Sending: {message}")
        print(f"{prefix} {message}") # Ensure visibility in CLI tests

# Singleton
_instance = None

def get_notification_manager() -> NotificationManager:
    global _instance
    if _instance is None:
        _instance = NotificationManager()
    return _instance
