"""
PPLI Simulation - Phase 79.
Private Placement Life Insurance calculator.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PPLISimulator:
    """Simulates PPLI benefits."""
    
    @staticmethod
    def calculate_tax_deferral(
        investment: float,
        years: int,
        growth_rate: float = 0.07,
        tax_rate: float = 0.37
    ) -> Dict[str, float]:
        # PPLI grows tax-free
        ppli_value = investment * ((1 + growth_rate) ** years)
        
        # Taxable account pays taxes on gains annually
        after_tax_rate = growth_rate * (1 - tax_rate)
        taxable_value = investment * ((1 + after_tax_rate) ** years)
        
        return {
            "ppli_value": round(ppli_value, 2),
            "taxable_value": round(taxable_value, 2),
            "tax_savings": round(ppli_value - taxable_value, 2)
        }
