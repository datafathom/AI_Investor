"""
Lock Manager Service.
Tracks and enforces time-based trading cooldowns (Emotional Muffler).
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

class LockManager:
    """
    Manages systems-level trading locks.
    """

    def __init__(self):
        self.active_locks: Dict[str, datetime] = {} # user_id -> unlock_time

    def apply_lock(self, user_id: str, duration_hours: int = 4, reason: str = "TILT"):
        """
        Establish a hard lock for a specific duration.
        """
        unlock_time = datetime.now() + timedelta(hours=duration_hours)
        self.active_locks[user_id] = unlock_time
        logger.warning(f"BEHAVIORAL_LOCK: User {user_id} locked until {unlock_time} (Reason: {reason})")

    def is_user_locked(self, user_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if the user is currently subject to a cooldown.
        """
        if user_id not in self.active_locks:
            return False, None

        unlock_time = self.active_locks[user_id]
        if datetime.now() < unlock_time:
            time_remaining = unlock_time - datetime.now()
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return True, f"COOLING_OFF: System locked for {hours}h {minutes}m remaining."
        
        # Lock expired
        del self.active_locks[user_id]
        return False, None

    def clear_lock(self, user_id: str):
        """
        Remove a lock (Internal override use only).
        """
        if user_id in self.active_locks:
            del self.active_locks[user_id]
            logger.info(f"LOCK_CLEARED: Trading resumed for user {user_id}.")
