"""
Bond Ladder & Yield Curve Monitor - Phase 46.
Tracks bond ladder for income stability.
"""
import logging
from typing import Dict, Any, List
from datetime import date

logger = logging.getLogger(__name__)

class BondLadder:
    """Manages bond ladder structure."""
    
    def __init__(self):
        self.bonds: List[Dict[str, Any]] = []
    
    def add_bond(self, maturity_date: date, face_value: float, coupon: float):
        self.bonds.append({
            "maturity": maturity_date,
            "face_value": face_value,
            "coupon": coupon
        })
    
    def get_annual_income(self) -> float:
        return sum(b["face_value"] * b["coupon"] for b in self.bonds)
    
    def get_maturing_soon(self, within_months: int = 12) -> List[Dict[str, Any]]:
        from datetime import timedelta
        cutoff = date.today() + timedelta(days=within_months * 30)
        return [b for b in self.bonds if b["maturity"] <= cutoff]
