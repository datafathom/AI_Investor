"""
Spam Detector Service.
Detects frantic inputs or failed override attempts.
"""
import logging
from typing import Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SpamDetector:
    """Detects input spam/rage clicking."""
    
    def __init__(self):
        self.attempt_log = []
        self.threshold = 10 # actions
        self.window_seconds = 10 # seconds
        self.cooldown_active = False

    def log_attempt(self, user_id: str, action_type: str) -> Dict[str, Any]:
        now = datetime.now()
        self.attempt_log.append(now)
        
        # Prune old logs
        window_start = now - timedelta(seconds=self.window_seconds)
        self.attempt_log = [t for t in self.attempt_log if t > window_start]
        
        count = len(self.attempt_log)
        
        if count >= self.threshold:
            logger.warning(f"SPAM_DETECTED: {count} actions in {self.window_seconds}s for user {user_id}")
            return {"spam_detected": True, "action": "BLOCK_INPUT"}
            
        return {"spam_detected": False, "count": count}
