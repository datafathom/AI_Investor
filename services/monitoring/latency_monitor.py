"""
Latency Monitor Service.
Measures end-to-end processing time for market events.
"""
import time
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class LatencyMonitor:
    """
    Tracks and reports timing metrics for the Redpanda-Postgres pipeline.
    """
    def __init__(self):
        self.stats: Dict[str, List[float]] = {}
    def record_endpoint_latency(self, endpoint: str, duration: float):
        """Record latency for a specific API endpoint."""
        if endpoint not in self.stats:
            self.stats[endpoint] = []
        self.stats[endpoint].append(duration)
        if len(self.stats[endpoint]) > 500:
            self.stats[endpoint].pop(0)

    def _calculate_percentile(self, values: List[float], percentile: float) -> float:
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(percentile * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]

    def get_latency_summary(self) -> Dict[str, Any]:
        """Aggregate stats for all tracked endpoints."""
        summary = {"endpoints": []}
        for path, values in self.stats.items():
            summary["endpoints"].append({
                "path": path,
                "p50": round(self._calculate_percentile(values, 0.50) * 1000, 2),
                "p95": round(self._calculate_percentile(values, 0.95) * 1000, 2),
                "p99": round(self._calculate_percentile(values, 0.99) * 1000, 2),
                "count": len(values)
            })
        return summary

    def get_endpoint_histogram(self, endpoint: str) -> Dict[str, Any]:
        """Generate histogram bins for an endpoint."""
        values = [v * 1000 for v in self.stats.get(endpoint, [])]
        if not values: return {"buckets": []}
        
        bins = [0, 50, 100, 250, 500, 1000, 2500, 5000]
        histogram = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins)-1)}
        histogram["5000+"] = 0
        
        for v in values:
            found = False
            for i in range(len(bins)-1):
                if bins[i] <= v < bins[i+1]:
                    histogram[f"{bins[i]}-{bins[i+1]}"] += 1
                    found = True
                    break
            if not found:
                histogram["5000+"] += 1
                
        return {"buckets": [{"range": k, "count": v} for k, v in histogram.items()]}

# Global Instance
latency_monitor = LatencyMonitor()

def get_latency_monitor() -> LatencyMonitor:
    return latency_monitor
