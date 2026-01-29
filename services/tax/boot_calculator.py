
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BootCalculator:
    """
    Calculates the taxable 'boot' received in a 1031 exchange.
    Boot occurs when debt is reduced without cash offset or when cash is pulled out.
    """
    
    def calculate_taxable_boot(
        self,
        cash_boot: Decimal,
        mortgage_boot: Decimal,
        offsetting_cash_added: Decimal = Decimal('0.00')
    ) -> Dict[str, Any]:
        """
        Calculates net taxable boot.
        """
        # Mortgage boot can be offset by cash added, but cash boot cannot 
        # be offset by mortgage added.
        net_mortgage_boot = max(Decimal('0.00'), mortgage_boot - offsetting_cash_added)
        total_boot = cash_boot + net_mortgage_boot
        
        logger.info(f"Boot Calculation: Cash={cash_boot}, Mortgage={mortgage_boot}, Offset={offsetting_cash_added}, Result=${total_boot}")
        
        return {
            "cash_boot": cash_boot,
            "mortgage_boot": mortgage_boot,
            "offset_applied": offsetting_cash_added,
            "net_taxable_boot": total_boot,
            "tax_estimate_20pct": (total_boot * Decimal('0.20')).quantize(Decimal('0.01'))
        }
