"""
SAFE Note Ownership Calculator.
Calculates startup equity based on caps and discounts.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SAFECalculator:
    """Calculates conversion ownership for SAFEs."""
    
    def calculate_ownership(self, investment: float, val_cap: float, discount_rate: float, pre_money_val: float) -> Dict[str, Any]:
        # Conversion price based on cap
        price_cap = val_cap # simplified
        # Conversion price based on discount
        price_discount = pre_money_val * (1.0 - discount_rate)
        
        applied_val = min(price_cap, price_discount)
        ownership = (investment / (applied_val + investment)) # post-money
        
        return {
            "effective_valuation": applied_val,
            "equity_percentage": round(ownership * 100, 4),
            "mechanism_triggered": "CAP" if price_cap < price_discount else "DISCOUNT"
        }
