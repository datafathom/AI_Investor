import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DarkPoolTapeService:
    """
    Ingests and analyzes dark pool (off-exchange) trades.
    Dark pools represent 40%+ of market volume.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DarkPoolTapeService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.adf_code = "D"  # ADF exchange code for dark pools
        logger.info("DarkPoolTapeService initialized")

    def filter_dark_prints(self, tape_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter tape for dark pool (off-exchange) prints."""
        return [
            trade for trade in tape_data 
            if trade.get("exchange") == self.adf_code
        ]

    def detect_block_clusters(
        self, 
        dark_prints: List[Dict[str, Any]], 
        min_size: int = 10000, 
        time_window_minutes: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Detect clustering of similar-sized block trades.
        Institutions often split large orders into identical chunks.
        """
        clusters = []
        # Simplified detection - would use more sophisticated algo
        size_groups = {}
        for print_data in dark_prints:
            size = print_data.get("size", 0)
            if size >= min_size:
                if size not in size_groups:
                    size_groups[size] = []
                size_groups[size].append(print_data)
        
        for size, trades in size_groups.items():
            if len(trades) >= 3:  # 3+ identical size = cluster
                clusters.append({
                    "size": size,
                    "count": len(trades),
                    "total_volume": size * len(trades),
                    "type": "SPLIT_BLOCK"
                })
                logger.info(f"Detected block cluster: {len(trades)}x {size} shares")
        
        return clusters

    def get_significant_levels(
        self, 
        dark_prints: List[Dict[str, Any]], 
        min_volume_pct: float = 0.1
    ) -> List[Dict[str, float]]:
        """
        Identify price levels with significant dark pool activity.
        These levels often act as support/resistance.
        """
        level_volume = {}
        total_volume = sum(p.get("size", 0) for p in dark_prints)
        
        for print_data in dark_prints:
            price = round(print_data.get("price", 0), 2)
            size = print_data.get("size", 0)
            level_volume[price] = level_volume.get(price, 0) + size
        
        significant_levels = []
        for price, volume in level_volume.items():
            pct = volume / total_volume if total_volume > 0 else 0
            if pct >= min_volume_pct:
                significant_levels.append({"price": price, "volume": volume, "pct": pct})
        
        return sorted(significant_levels, key=lambda x: x["volume"], reverse=True)
