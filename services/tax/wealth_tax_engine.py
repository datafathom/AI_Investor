import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class WealthTaxEngine:
    """
    Simulates the 'Tax-on-Tax' spiral in wealth-tax jurisdictions (Norway, Spain, etc.).
    Models the liquidation impact where selling assets to pay tax triggers more tax liability.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WealthTaxEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("WealthTaxEngine initialized")

    def calculate_annual_liability(self, net_wealth: Decimal, rate: Decimal = Decimal('0.011')) -> Decimal:
        """
        Policy: Standard wealth tax bill (e.g., 1.1% for Norway).
        """
        return net_wealth * rate

    def simulate_tax_on_tax_spiral(self, tax_bill: Decimal, cgt_rate: Decimal = Decimal('0.378')) -> Dict[str, Any]:
        """
        Policy: To pay $X tax, you sell $Y assets. If selling $Y triggers CGT, 
        you must sell $Y = X / (1 - CGT_Rate).
        """
        total_liquidation_required = tax_bill / (Decimal('1') - cgt_rate)
        cgt_generated = total_liquidation_required - tax_bill
        
        logger.warning(f"TAX_LOG: Bill ${tax_bill:,.2f} requires ${total_liquidation_required:,.2f} sale (CGT: ${cgt_generated:,.2f})")
        
        return {
            "primary_tax_bill": round(tax_bill, 2),
            "liquidation_triggered_cgt": round(cgt_generated, 2),
            "total_liquidity_needed": round(total_liquidation_required, 2),
            "effective_wealth_tax_rate_w_cgt": round((total_liquidation_required / tax_bill) * Decimal('100'), 2)
        }
