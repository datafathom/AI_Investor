"""
Warden Health Log.
Persists health check results.
"""
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HealthLog:
    """Logs warden health checks."""
    
    def log_check(self, check_result: Dict[str, Any]):
        # In real app: Write to Postgres 'warden_logs'
        status = check_result.get("overall_status", "UNKNOWN")
        logger.info(f"WARDEN_CHECK_LOG: {status} - {check_result}")
