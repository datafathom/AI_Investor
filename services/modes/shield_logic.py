"""
Shield Logic.
Manages global defensive state.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ShieldLogic:
    """Manages system shield mode."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.shield_key = "system:shield_mode"
        
    def activate_shield(self, reason: str):
        self.redis.set(self.shield_key, "TRUE")
        self.redis.set(f"{self.shield_key}:reason", reason)
        logger.warning(f"SHIELD_ACTIVATED: {reason}")
        
    def deactivate_shield(self):
        self.redis.set(self.shield_key, "FALSE")
        logger.info("SHIELD_DEACTIVATED")
        
    def is_active(self) -> bool:
        return self.redis.get(self.shield_key) == "TRUE"
