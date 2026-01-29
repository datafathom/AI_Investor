import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BenchmarkService:
    """Retrieves lifestyle benchmarking data for various income groups."""
    
    BENCHMARKS = {
        "UPPER_MIDDLE": {
            "HOUSING_PCT": 0.25,
            "SAVINGS_PCT": 0.20,
            "EDUCATION_PCT": 0.10
        },
        "HNW": {
            "HOUSING_PCT": 0.15,
            "SAVINGS_PCT": 0.40,
            "TRAVEL_PCT": 0.10
        }
    }

    def get_benchmarks(self, peer_group: str) -> Dict[str, float]:
        return self.BENCHMARKS.get(peer_group, self.BENCHMARKS["UPPER_MIDDLE"])
