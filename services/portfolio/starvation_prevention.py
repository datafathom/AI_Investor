"""
Asset Starvation Prevention - Phase 30.
Ensures capital allocation across multiple assets.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class StarvationPrevention:
    """Prevents over-concentration in single assets."""
    
    @staticmethod
    def check_allocation(positions: List[Dict[str, Any]], max_single_asset_pct: float = 0.25) -> bool:
        if not positions:
            return True
        total_value = sum(p.get("value", 0) for p in positions)
        if total_value == 0:
            return True
        for pos in positions:
            if pos.get("value", 0) / total_value > max_single_asset_pct:
                return False
        return True
