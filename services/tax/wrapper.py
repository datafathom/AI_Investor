"""
Tax Wrapper Service.
Handles logic for tax-advantaged account types.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TaxWrapper:
    """Manages tax wrappers (401k, IRA)."""
    
    LIMITS = {
        "401k": 23000,
        "IRA": 7000,
        "HSA": 4150
    }
    
    def calculate_remaining_contribution(self, account_type: str, current_contribution: float) -> float:
        limit = self.LIMITS.get(account_type.upper(), 0)
        return max(0, limit - current_contribution)
        
    def estimate_tax_savings(self, amount: float, marginal_rate: float) -> float:
        return amount * marginal_rate
