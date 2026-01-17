"""
==============================================================================
FILE: services/monitoring/health_monitor.py
ROLE: System Physician
PURPOSE:
    Monitor vital system statistics to ensure the AI Investor is running
    on healthy infrastructure.
    
    1. Resource Tracking:
       - CPU Usage
       - Memory Usage
       - Disk Space
       
    2. Self-Healing Triggers:
       - Detects if a service is "Zombie" (mock logic for now).
       
ROADMAP: Phase 31 - Self-Healing & Observability
==============================================================================
"""

import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HealthMonitor:
    
    def get_system_vitals(self) -> Dict[str, Any]:
        """
        Get current system resource usage.
        """
        vitals = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "status": "HEALTHY"
        }
        
        # Simple heuristic for "Unhealthy"
        if vitals["cpu_percent"] > 90 or vitals["memory_percent"] > 90:
            vitals["status"] = "CRITICAL_LOAD"
            
        return vitals

    def check_service_health(self, service_name: str) -> bool:
        """
        Check if a specific service/process is running.
        (Mock implementation using random PIDs logic or loop check)
        """
        # In a real scenario, we'd check `docker ps` or PID files
        return True

# Singleton
_instance = None

def get_health_monitor() -> HealthMonitor:
    global _instance
    if _instance is None:
        _instance = HealthMonitor()
    return _instance
