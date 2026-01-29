"""
Index Fund Exposure Tracker - Phase 36.
Tracks exposure to index funds across accounts.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class IndexTracker:
    """Tracks index fund allocations."""
    
    def __init__(self):
        self.holdings: Dict[str, float] = {}
    
    def add_holding(self, index_name: str, value: float):
        self.holdings[index_name] = self.holdings.get(index_name, 0) + value
    
    def get_total_index_exposure(self) -> float:
        return sum(self.holdings.values())
    
    def get_allocation_pct(self, index_name: str, total_portfolio: float) -> float:
        if total_portfolio == 0:
            return 0.0
        return self.holdings.get(index_name, 0) / total_portfolio * 100
