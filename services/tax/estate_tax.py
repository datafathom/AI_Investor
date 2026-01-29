"""
Estate Tax Simulator.
Estimates death tax liability.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EstateTaxSim:
    """Simulates estate tax impact."""
    
    EXEMPTION_2024 = 13610000.0 # $13.61M
    MAX_RATE = 0.40 # 40%
    
    def calculate_liability(self, net_worth: float) -> Dict[str, Any]:
        taxable_estate = max(0, net_worth - self.EXEMPTION_2024)
        tax_bill = taxable_estate * self.MAX_RATE
        
        return {
            "net_worth": net_worth,
            "exemption": self.EXEMPTION_2024,
            "taxable_amount": taxable_estate,
            "estimated_tax": tax_bill,
            "effective_rate": (tax_bill / net_worth) if net_worth > 0 else 0
        }
