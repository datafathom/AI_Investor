"""
Alternatives Tracker.
Tracks Commodities, Crypto, and Art.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AlternativeAssets:
    """Tracks alternative asset classes."""
    
    def __init__(self):
        self.assets = {}
        
    def add_asset(self, asset_type: str, value: float):
        self.assets[asset_type] = self.assets.get(asset_type, 0) + value
        
    def get_total_exposure(self) -> float:
        return sum(self.assets.values())
