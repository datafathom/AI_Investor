"""
Multi-Currency Cash Management - Phase 56.
Manages FX exposure and multi-currency holdings.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CurrencyManager:
    """Manages multi-currency positions."""
    
    def __init__(self):
        self.balances: Dict[str, float] = {}
        self.fx_rates: Dict[str, float] = {"USD": 1.0}
    
    def add_balance(self, currency: str, amount: float):
        self.balances[currency] = self.balances.get(currency, 0) + amount
    
    def set_fx_rate(self, currency: str, rate: float):
        self.fx_rates[currency] = rate
    
    def get_total_usd(self) -> float:
        total = 0.0
        for curr, amt in self.balances.items():
            rate = self.fx_rates.get(curr, 1.0)
            total += amt * rate
        return total
