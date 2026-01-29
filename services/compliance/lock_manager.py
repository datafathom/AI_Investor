"""
Lock Manager Service.
Enforces cooling-off periods and behavioral locks.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LockManager:
    """Manages trading locks."""
    
    def __init__(self, db_session = None):
        self.db = db_session 
        # In a real app, this would use the DB session to query the table created in migration 22

    def is_locked(self, user_id: str) -> Dict[str, Any]:
        """Check if user is currently locked out."""
        # MOCK: In production, query SELECT * FROM trading_locks WHERE user_id = ... AND is_active = TRUE AND unlock_time > NOW()
        # For now, we simulate no lock unless set in memory
        return {"locked": False, "reason": None, "remaining_minutes": 0}

    def apply_lock(self, user_id: str, lock_type: str, duration_minutes: int, reason: str) -> Dict[str, Any]:
        """Apply a new lock."""
        unlock_time = datetime.now() + timedelta(minutes=duration_minutes)
        logger.warning(f"LOCK_APPLIED: User {user_id} locked for {duration_minutes}m. Type: {lock_type}. Reason: {reason}")
        
        # MOCK: Insert into DB
        return {
            "success": True,
            "lock_id": "mock-lock-uuid",
            "unlock_time": unlock_time.isoformat()
        }
