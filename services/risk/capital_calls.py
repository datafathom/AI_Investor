"""
Capital Call Tracker.
Tracks committed vs called capital for PE/VC.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CapitalCallTracker:
    """Tracks dry powder liabilities."""
    
    def __init__(self):
        self.commitments = {}
        
    def add_commitment(self, fund_name: str, amount: float):
        self.commitments[fund_name] = {"total": amount, "called": 0.0}
        
    def log_call(self, fund_name: str, called_amount: float):
        if fund_name in self.commitments:
            self.commitments[fund_name]["called"] += called_amount
            
    def get_uncalled_liability(self) -> float:
        total = 0
        for info in self.commitments.values():
            total += (info["total"] - info["called"])
        return total
