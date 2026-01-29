"""
SBLOC Feasibility Calculator.
Compares borrowing against securities vs liquidation.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SBLOCCalculator:
    """Calculates borrowing power and risk."""
    
    def compare_borrow_vs_sell(self, amount_needed: float, borrow_rate: float, cap_gains_rate: float, portfolio_yield: float) -> Dict[str, Any]:
        cost_borrow = amount_needed * borrow_rate
        
        # If selling, need to gross up for tax
        gross_up_sell = amount_needed / (1.0 - cap_gains_rate)
        tax_bill = gross_up_sell - amount_needed
        lost_compounding = gross_up_sell * portfolio_yield
        
        cost_sell = tax_bill + lost_compounding
        
        return {
            "annual_borrow_cost": round(cost_borrow, 2),
            "upfront_sell_tax": round(tax_bill, 2),
            "recommendation": "BORROW_SBLOC" if cost_borrow < cost_sell else "SELL_ASSET"
        }
