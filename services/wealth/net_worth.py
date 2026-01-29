"""
Multi-Asset Net Worth Dashboard.
Aggregates wealth from all sources.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NetWorthAggregator:
    """Aggregates total net worth."""
    
    def __init__(self):
        self.sources = {}
        
    def add_balance(self, source: str, amount: float):
        self.sources[source] = amount
        
    def calculate_total(self) -> Dict[str, Any]:
        total = sum(self.sources.values())
        
        breakdown = {k: v for k, v in sorted(self.sources.items(), key=lambda item: item[1], reverse=True)}
        
        return {
            "total_net_worth": round(total, 2),
            "breakdown": breakdown
        }
