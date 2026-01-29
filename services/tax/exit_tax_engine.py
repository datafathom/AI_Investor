import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExitTaxEngine:
    """
    Models the 'Expatriation Tax' (IRS 877A) for Covered Expatriates.
    Calculates tax based on a 'Mark-to-Market' phantom sale of worldwide assets.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ExitTaxEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("ExitTaxEngine initialized")

    def determine_expat_status(self, net_worth: Decimal, avg_income_tax_5yr: Decimal) -> Dict[str, Any]:
        """
        Policy: Net Worth > $2M OR Avg Tax > $190k (2024 index) = COVERED EXPAT.
        """
        nw_test = net_worth > Decimal('2000000')
        tax_test = avg_income_tax_5yr > Decimal('190000')
        
        is_covered = nw_test or tax_test
        
        return {
            "net_worth": round(net_worth, 2),
            "avg_tax_liability": round(avg_income_tax_5yr, 2),
            "is_covered_expatriate": is_covered,
            "exit_tax_regime": "MARK_TO_MARKET" if is_covered else "NONE"
        }

    def calculate_phantom_sale_liability(self, current_fmv: Decimal, cost_basis: Decimal, annual_exclusion: Decimal = Decimal('866000')) -> Dict[str, Any]:
        """
        Core Calculation: (Total Unrealized Gains - Exclusion) * LTCG Rate.
        """
        total_gain = max(Decimal('0'), current_fmv - cost_basis)
        taxable_gain = max(Decimal('0'), total_gain - annual_exclusion)
        estimated_tax = taxable_gain * Decimal('0.238') # 20% LTCG + 3.8% NIIT
        
        logger.info(f"TAX_LOG: Phantom sale of ${current_fmv:,.2f} creates ${estimated_tax:,.2f} exit tax liability.")
        
        return {
            "total_unrealized_gain": round(total_gain, 2),
            "exemption_applied": round(annual_exclusion, 2),
            "taxable_exit_gain": round(taxable_gain, 2),
            "estimated_tax_bill": round(estimated_tax, 2)
        }
