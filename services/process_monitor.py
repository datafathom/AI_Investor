"""
Process Monitor Service.
Tracks agent PIDs and system resource utilization.
"""
import os
import logging
import psutil
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ProcessMonitor:
    """
    Monitors OS level stats for agent processes.
    """

    @staticmethod
    def get_process_stats(pid: int) -> Optional[Dict[str, Any]]:
        """Retrieve resource usage for a specific PID."""
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                return {
                    'pid': pid,
                    'name': proc.name(),
                    'status': proc.status(),
                    'cpu_pct': proc.cpu_percent(),
                    'mem_mb': proc.memory_info().rss / (1024 * 1024),
                    'threads': proc.num_threads(),
                    'is_running': proc.is_running()
                }
        except psutil.NoSuchProcess:
            logger.error(f"Process {pid} not found.")
            return None
        except Exception as e:
            logger.error(f"Failed to monitor PID {pid}: {e}")
            return None

    @staticmethod
    def is_pid_alive(pid: int) -> bool:
        """Check if PID is active."""
        return psutil.pid_exists(pid)
