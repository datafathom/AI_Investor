"""
Safe Mode Bootstrapper.
Ensures system boots safely if DB is down.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SafeBoot:
    """Safe mode bootstrapper."""
    
    SAFE_CONFIG = {
        "max_position_size_pct": 0.0,
        "daily_drawdown_limit_pct": 0.0,
        "max_leverage_ratio": 1.0,
        "mode": "SAFE_MODE"
    }
    
    @staticmethod
    def get_safe_config() -> Dict[str, Any]:
        logger.critical("SAFE_BOOT_TRIGGERED: System operating in SAFE MODE.")
        return SafeBoot.SAFE_CONFIG
