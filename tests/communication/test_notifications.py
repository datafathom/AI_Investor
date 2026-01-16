
import pytest
from services.communication.notification_manager import NotificationManager, AlertPriority, NotificationChannel

class TestNotificationManager:
    
    def test_alert_routing_critical(self):
        manager = NotificationManager()
        # Clean history
        manager.history = []
        
        manager.send_alert("System Crash Imminent", AlertPriority.CRITICAL)
        
        assert len(manager.history) == 1
        record = manager.history[0]
        assert record['priority'] == "CRITICAL"
        assert NotificationChannel.SMS.value in record['channels']
        assert NotificationChannel.EMAIL.value in record['channels']
        
    def test_alert_routing_info(self):
        manager = NotificationManager()
        manager.history = []
        
        manager.send_alert("Market Open", AlertPriority.INFO)
        
        assert len(manager.history) == 1
        record = manager.history[0]
        assert record['priority'] == "INFO"
        assert NotificationChannel.SMS.value not in record['channels']
        assert NotificationChannel.CONSOLE.value in record['channels']
