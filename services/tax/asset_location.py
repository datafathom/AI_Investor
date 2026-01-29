"""
Asset Location Optimizer - Phase 50.
Places assets in optimal account types for tax efficiency.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AssetLocationOptimizer:
    """Optimizes asset placement for tax efficiency."""
    
    TAX_EFFICIENT = ["index_funds", "etfs", "muni_bonds"]
    TAX_INEFFICIENT = ["bonds", "reits", "active_funds"]
    
    @staticmethod
    def recommend_location(asset_type: str) -> str:
        if asset_type.lower() in AssetLocationOptimizer.TAX_INEFFICIENT:
            return "TAX_ADVANTAGED"  # 401k, IRA
        return "TAXABLE"  # Brokerage
