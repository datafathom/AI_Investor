
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TaxBracketSimulator:
    """
    Simulates capital gains tax brackets including NIIT (Net Investment Income Tax).
    """
    
    def simulate_tax_bill(self, gain_amount: Decimal, annual_income: Decimal) -> Dict[str, Any]:
        """
        Calculates estimate tax rate based on income levels.
        """
        # Threshold for 3.8% NIIT (Obamacare Tax) for Single Filer: $200k
        niit_threshold = Decimal('200000.00')
        
        base_rate = Decimal('0.15')
        if annual_income > Decimal('500000.00'):
            base_rate = Decimal('0.20')
            
        niit_applied = annual_income > niit_threshold
        total_rate = base_rate + (Decimal('0.038') if niit_applied else Decimal('0.00'))
        
        estimated_tax = gain_amount * total_rate
        
        logger.info(f"Tax Sim: Gain=${gain_amount}, Income=${annual_income}, Rate={total_rate}, Tax=${estimated_tax}")
        
        return {
            "base_capital_gains_rate": float(base_rate),
            "niit_applied": niit_applied,
            "total_marginal_rate": float(total_rate),
            "estimated_tax_liability": float(estimated_tax)
        }
