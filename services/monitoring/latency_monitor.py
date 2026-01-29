"""
Latency Monitor Service.
Measures end-to-end processing time for market events.
"""
import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class LatencyMonitor:
    """
    Tracks and reports timing metrics for the Redpanda-Postgres pipeline.
    """
    def __init__(self):
        # symbol -> [latencies]
        self.stats: Dict[str, List[float]] = {}

    def record_latency(self, symbol: str, start_time: float):
        """
        Record and log the time taken since the original event timestamp.
        """
        duration = time.time() - start_time
        if symbol not in self.stats:
            self.stats[symbol] = []
        
        self.stats[symbol].append(duration)
        
        # Maintain small window for rolling average
        if len(self.stats[symbol]) > 100:
            self.stats[symbol].pop(0)

        # Log significant lag
        if duration > 0.200: # 200ms
            logger.warning(f"High E2E Latency for {symbol}: {duration*1000:.1f}ms")

    def get_average_latency(self, symbol: str) -> float:
        """Calculate mean latency in seconds."""
        if symbol not in self.stats or not self.stats[symbol]:
            return 0.0
        return sum(self.stats[symbol]) / len(self.stats[symbol])

# Global Instance
latency_monitor = LatencyMonitor()
