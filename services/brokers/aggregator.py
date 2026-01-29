"""
Multi-Broker Aggregator - Phase 31.
Consolidates positions across multiple brokers.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BrokerAggregator:
    """Aggregates data from multiple brokers."""
    
    def __init__(self):
        self.brokers: Dict[str, Dict[str, Any]] = {}
    
    def register_broker(self, name: str, config: Dict[str, Any]):
        self.brokers[name] = config
    
    def get_total_equity(self) -> float:
        return sum(b.get("equity", 0) for b in self.brokers.values())
    
    def get_all_positions(self) -> List[Dict[str, Any]]:
        positions = []
        for broker, config in self.brokers.items():
            positions.extend(config.get("positions", []))
        return positions
