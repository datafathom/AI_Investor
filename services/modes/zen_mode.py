"""
The Homeostasis Zen Mode - Phase 68.
System-wide calm mode.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ZenMode:
    """System-wide calm mode controller."""
    
    def __init__(self):
        self.active = False
        self.reason = ""
    
    def activate(self, reason: str):
        self.active = True
        self.reason = reason
        logger.info(f"ZEN_MODE_ACTIVATED: {reason}")
    
    def deactivate(self):
        self.active = False
        self.reason = ""
    
    def get_status(self) -> Dict[str, Any]:
        return {"active": self.active, "reason": self.reason}
