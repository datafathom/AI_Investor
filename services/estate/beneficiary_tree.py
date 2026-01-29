"""
Beneficiary Allocation Tree - Phase 82.
Visualizes beneficiary allocation.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class BeneficiaryTree:
    """Beneficiary allocation tree."""
    
    def __init__(self):
        self.primary: List[Dict[str, Any]] = []
        self.contingent: List[Dict[str, Any]] = []
    
    def add_primary(self, name: str, pct: float):
        self.primary.append({"name": name, "percentage": pct})
    
    def add_contingent(self, name: str, pct: float):
        self.contingent.append({"name": name, "percentage": pct})
    
    def validate(self) -> bool:
        primary_total = sum(b["percentage"] for b in self.primary)
        contingent_total = sum(b["percentage"] for b in self.contingent)
        return abs(primary_total - 100) < 0.01 and (not self.contingent or abs(contingent_total - 100) < 0.01)
