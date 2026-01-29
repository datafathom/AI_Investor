
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ILITBenefitCalculator:
    """
    Calculates estate tax savings from an ILIT.
    """
    
    def calculate_savings(self, death_benefit: Decimal, estate_rate: Decimal = Decimal('0.40')) -> Dict[str, Any]:
        """
        Savings = Death Benefit * Estate Tax Rate (40% default).
        """
        savings = death_benefit * estate_rate
        
        logger.info(f"ILIT Benefit: Policy=${death_benefit}, Rate={estate_rate}, TaxSavings=${savings}")
        
        return {
            "death_benefit": float(death_benefit),
            "estate_tax_rate": float(estate_rate),
            "estimated_tax_savings": float(savings),
            "net_liquidity_increase": float(savings)
        }
