"""
Warden Override Handler.
Handles emergency manual overrides of the system freeze.
"""
import logging
from typing import Dict, Any
from services.auth.mfa_service import MFAService
from services.infrastructure.redis_lock import RedisLock

logger = logging.getLogger(__name__)

class OverrideHandler:
    """Handles system overrides."""
    
    def __init__(self, mfa_service: MFAService, redis_lock: RedisLock):
        self.mfa = mfa_service
        self.redis = redis_lock
        
    def request_override(self, user_id: str, mfa_token: str, reason: str) -> Dict[str, Any]:
        """
        Request to override a system freeze (Zen Mode).
        requires valid MFA token.
        """
        if not self.mfa.verify_token(mfa_token):
            logger.warning(f"OVERRIDE_FAILED: Invalid MFA for user {user_id}")
            return {"success": False, "error": "Invalid MFA Token"}
            
        logger.warning(f"OVERRIDE_GRANTED: System freeze overridden by {user_id}. Reason: {reason}")
        
        # Release the global lock
        try:
            self.redis.release_lock("global_trading_lock")
            return {"success": True, "message": "System freeze lifted."}
        except Exception as e:
            logger.error(f"OVERRIDE_ERROR: Failed to release lock: {e}")
            return {"success": False, "error": str(e)}
