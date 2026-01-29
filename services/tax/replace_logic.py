"""
Tax Harvesting: Automated Replace Logic - Phase 86.
Automatically replaces harvested positions.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ReplaceLogic:
    """Automated replacement for harvested positions."""
    
    REPLACEMENTS = {
        "SPY": "VOO",
        "QQQ": "QQQM",
        "VTI": "ITOT",
        "AGG": "BND"
    }
    
    @staticmethod
    def get_replacement(symbol: str) -> str:
        return ReplaceLogic.REPLACEMENTS.get(symbol, symbol)
    
    @staticmethod
    def is_substantially_identical(a: str, b: str) -> bool:
        # Same underlying = substantially identical
        identical_pairs = [("SPY", "IVV"), ("QQQ", "QQQM")]
        return any((a in pair and b in pair) for pair in identical_pairs)
