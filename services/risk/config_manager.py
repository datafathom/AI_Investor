"""
Configuration Manager Service.
Synchronizes and hydrates global risk parameters from the Postgres Guardrail schema.
"""
import logging
from typing import Dict, Any, Optional

from services.security.config_integrity import ConfigIntegrity

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    State manager for versioned risk configurations.
    """

    def __init__(self):
        self._active_config: Dict[str, Any] = {}
        self._active_hash: str = ""
        self.safe_mode = False

    def hydrate_from_db(self, db_record: Dict[str, Any], signed_hash: str):
        """
        Validate and load a new configuration state.
        """
        # 1. Verify Integrity
        if not ConfigIntegrity.verify_integrity(db_record, signed_hash):
            logger.error("HYDRATION_FAILED: Configuration integrity check failed. Entering SAFE_MODE.")
            self.safe_mode = True
            self._active_config = self._get_safe_config()
            return

        # 2. Update local state
        self._active_config = db_record
        self._active_hash = signed_hash
        self.safe_mode = False
        logger.info(f"CONFIG_HYDRATED: New risk state loaded (ID: {db_record.get('id')})")

    def get_param(self, key: str, default: Any = None) -> Any:
        """
        Fetch a risk parameter from the active state.
        """
        return self._active_config.get(key, default)

    def _get_safe_config(self) -> Dict[str, Any]:
        """
        Default parameters for Safe Mode (0% Risk).
        """
        return {
            "max_position_size_pct": 0.0,
            "daily_drawdown_limit_pct": 0.0,
            "max_leverage_ratio": 1.0,
            "status": "SAFE_MODE: INTEGRITY_FAIL"
        }
