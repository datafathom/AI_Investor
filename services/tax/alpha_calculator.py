"""
Tax Savings Alpha Calculator - Phase 81.
Calculates tax savings as investment alpha.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TaxAlphaCalculator:
    """Calculates tax savings alpha."""
    
    @staticmethod
    def calculate_alpha(harvested_losses: float, tax_rate: float, portfolio_value: float) -> Dict[str, float]:
        tax_savings = harvested_losses * tax_rate
        alpha_bps = (tax_savings / portfolio_value) * 10000 if portfolio_value > 0 else 0
        
        return {
            "harvested_losses": harvested_losses,
            "tax_savings": tax_savings,
            "alpha_bps": round(alpha_bps, 2)
        }
