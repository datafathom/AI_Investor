"""
Mortgage Amortization Tracker.
Calculates principal/interest breakdown to update equity.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AmortizationTracker:
    """Tracks mortgage paydown progress."""
    
    def get_equity_gain(self, balance: float, rate: float, payment: float) -> float:
        monthly_rate = rate / 12
        interest = balance * monthly_rate
        principal = payment - interest
        return max(0, principal)
