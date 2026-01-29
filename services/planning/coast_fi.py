"""
Coast FI Calculator.
Calculates net worth required to stop saving while maintaining retirement date.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CoastFICalc:
    """Calculates 'Coast' status."""
    
    def calculate_coast(self, current_age: int, retire_age: int, target_amount: float, expected_growth: float) -> float:
        years_to_grow = retire_age - current_age
        required_today = target_amount / ((1 + expected_growth) ** years_to_grow)
        return round(required_today, 2)
