import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class NegativeSelectionFilter:
    """Identifies companies that are included in small-cap indices primarily due to poor performance."""
    
    def filter_laggards(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        laggards = []
        for stock in listings:
            # Relegation trigger: high market cap previously, but dropped into Russell 2000 range
            if stock.get("prev_rank") and stock.get("prev_rank") <= 1000 and stock.get("curr_rank") > 1000:
                laggards.append({
                    "ticker": stock.get("ticker"),
                    "reason": "RELEGATED_FROM_LARGE_CAP",
                    "performance_12m": stock.get("perf_12m")
                })
        
        logger.info(f"ANALYSIS_LOG: Found {len(laggards)} negatively selected laggards.")
        return laggards
