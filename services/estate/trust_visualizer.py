"""
Trust Structure Visualizer - Phase 87.
Visualizes trust structures.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TrustVisualizer:
    """Visualizes trust structures."""
    
    def __init__(self):
        self.trusts: List[Dict[str, Any]] = []
    
    def add_trust(self, name: str, trust_type: str, assets: float):
        self.trusts.append({"name": name, "type": trust_type, "assets": assets})
    
    def get_structure(self) -> Dict[str, Any]:
        return {
            "total_trusts": len(self.trusts),
            "total_assets": sum(t["assets"] for t in self.trusts),
            "by_type": self._group_by_type()
        }
    
    def _group_by_type(self) -> Dict[str, float]:
        by_type = {}
        for t in self.trusts:
            by_type[t["type"]] = by_type.get(t["type"], 0) + t["assets"]
        return by_type
