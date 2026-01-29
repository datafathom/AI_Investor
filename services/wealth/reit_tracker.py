"""
REIT Tracker Service.
Tracks Real Estate Investment Trusts.
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class REITTracker:
    """Tracks REIT exposure and income."""
    
    def calculate_yield(self, holdings: List[Dict[str, Any]]) -> float:
        total_value = sum(h["value"] for h in holdings)
        total_income = sum(h["value"] * h["dividend_yield"] for h in holdings)
        
        if total_value == 0:
            return 0.0
            
        return (total_income / total_value) * 100
