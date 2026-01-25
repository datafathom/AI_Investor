from datetime import datetime
import logging
from typing import Dict, Any

from services.communication.message_bus import MessageBus

logger = logging.getLogger(__name__)

class KillSwitchService:
    """
    Service to handle global system kill switch events.
    Broadcasts EMERGENCY_KILL signals to all agents and services.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KillSwitchService, cls).__new__(cls)
            cls._instance.bus = MessageBus()
            cls._instance.is_frozen = False
        return cls._instance

    def activate_kill_switch(self, user_id: str) -> Dict[str, Any]:
        """
        Activates the global kill switch.
        
        Args:
            user_id: The ID of the user initiating the kill switch.
            
        Returns:
            Dict containing the status of the operation.
        """
        logger.critical(f"KILL SWITCH ACTIVATED BY USER: {user_id}")
        
        self.is_frozen = True
        
        # timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # Broadcast High Priority Emergency Message
        message = {
            "type": "EMERGENCY_KILL",
            "timestamp": timestamp,
            "userId": user_id,
            "action": "HALT_ALL_ACTIVITY"
        }
        
        # Publish to system-wide event bus (Kafka/internal)
        # Assuming MessageBus has a publish method that handles priority
        try:
            self.bus.publish("system", "emergency", message)
            logger.info("EMERGENCY_KILL signal broadcasted successfully")
        except Exception as e:
            logger.error(f"Failed to broadcast EMERGENCY_KILL signal: {e}")
            return {"status": "error", "message": str(e)}
            
        return {
            "status": "success", 
            "message": "SYSTEM FROZEN. Emergency procedures initiated.",
            "timestamp": timestamp
        }

    def deactivate_kill_switch(self, passcode: str) -> bool:
        """
        Deactivates the kill switch if passcode is correct.
        This is a placeholder validation.
        """
        # In a real system, validate against a secure store
        # For now, hardcoded for Phase 5 demo
        if passcode == "123456": # Default dev passcode
            self.is_frozen = False
            logger.info("Kill switch deactivated via passcode")
            return True
        return False
        
    def get_status(self) -> Dict[str, Any]:
        return {"is_frozen": self._instance.is_frozen}
