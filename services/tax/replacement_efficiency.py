"""
Replacement Efficiency Tracker - Phase 96.
Tracks efficiency of tax-loss replacement.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ReplacementEfficiency:
    """Tracks replacement efficiency."""
    
    def __init__(self):
        self.replacements: List[Dict[str, Any]] = []
    
    def log_replacement(self, sold: str, bought: str, tracking_error: float):
        self.replacements.append({"sold": sold, "bought": bought, "tracking_error": tracking_error})
    
    def get_avg_tracking_error(self) -> float:
        if not self.replacements:
            return 0.0
        return sum(r["tracking_error"] for r in self.replacements) / len(self.replacements)
