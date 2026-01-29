"""
System Health & Hardware Telemetry - Phase 62.
Monitors system health metrics.
"""
import logging
import psutil
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SystemTelemetry:
    """Monitors system health."""
    
    @staticmethod
    def get_health() -> Dict[str, Any]:
        return {
            "cpu_pct": psutil.cpu_percent() if hasattr(psutil, 'cpu_percent') else 0,
            "memory_pct": psutil.virtual_memory().percent if hasattr(psutil, 'virtual_memory') else 0,
            "status": "HEALTHY"
        }
