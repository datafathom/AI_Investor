"""
==============================================================================
FILE: services/notifications/notification_preferences.py
ROLE: Settings Manager
PURPOSE: Manages user notification channels and frequency.
==============================================================================
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class NotificationPreferences:
    """
    Manager for user notification settings (SMS, Email, Slack).
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationPreferences, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True
        self._preferences = {
            "sms": {
                "enabled": False,
                "phone_number": None,
                "verified": False,
                "alert_types": ["margin_call", "liquidation"]
            },
            "email": {
                "enabled": True,
                "address": "user@example.com",
                "alert_types": ["trade_fill", "daily_report", "security_alert"]
            }
        }

    def get_preferences(self) -> Dict[str, Any]:
        return self._preferences

    def update_sms_preferences(self, phone: str = None, enabled: bool = None, alert_types: List[str] = None):
        """Update SMS settings."""
        if phone is not None:
            self._preferences["sms"]["phone_number"] = phone
            self._preferences["sms"]["verified"] = False # Reset verification on change
        if enabled is not None:
            self._preferences["sms"]["enabled"] = enabled
        if alert_types is not None:
            self._preferences["sms"]["alert_types"] = alert_types
        
        logger.info(f"NotificationPreferences updated for SMS: {self._preferences['sms']}")

    def verify_phone(self, code: str) -> bool:
        """Mock verification of phone number."""
        if code == "123456":
            self._preferences["sms"]["verified"] = True
            logger.info("Phone number verified successfully.")
            return True
        return False

def get_notification_preferences() -> NotificationPreferences:
    return NotificationPreferences()
 flagship_preferences = get_notification_preferences()
