
import logging
import time
from typing import Dict, Any
from utils.database_manager import get_database_manager
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)

class HealthCheckService:
    """
    Service for monitoring the health of all backing services.
    Used for staging smoke tests and production monitoring.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HealthCheckService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = get_database_manager()
        self.cache = get_cache_service()

    def check_postgres(self) -> Dict[str, Any]:
        """Checks connectivity to PostgreSQL."""
        try:
            start = time.time()
            with self.db.pg_cursor() as cur:
                cur.execute("SELECT 1")
            return {"status": "UP", "latency_ms": round((time.time() - start) * 1000, 2)}
        except Exception as e:
            logger.error(f"HealthCheck: Postgres DOWN: {e}")
            return {"status": "DOWN", "error": str(e)}

    def check_redis(self) -> Dict[str, Any]:
        """Checks connectivity to Redis."""
        try:
            start = time.time()
            self.cache.get("healthcheck_ping")
            return {"status": "UP", "latency_ms": round((time.time() - start) * 1000, 2)}
        except Exception as e:
            logger.error(f"HealthCheck: Redis DOWN: {e}")
            return {"status": "DOWN", "error": str(e)}

    def get_full_status(self) -> Dict[str, Any]:
        """Aggregates health status of all systems."""
        status = {
            "postgres": self.check_postgres(),
            "redis": self.check_redis(),
            "timestamp": time.time()
        }
        
        # Overall status
        all_up = all(v["status"] == "UP" for k, v in status.items() if isinstance(v, dict))
        status["overall"] = "UP" if all_up else "DEGRADED"
        
        return status

def get_health_check_service() -> HealthCheckService:
    return HealthCheckService()
