import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TotalWealthCalculator:
    """
    Unified metric engine for UHNW clients.
    Combines Liquid Portfolios, Irrevocable Trusts, PPLI Cash Value, and Private Assets.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TotalWealthCalculator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("TotalWealthCalculator initialized")

    def aggregate_net_worth(
        self, 
        liquid_assets: Decimal, 
        trust_assets: Decimal, 
        insurance_cash_value: Decimal,
        private_placements: Decimal
    ) -> Dict[str, Any]:
        """
        Policy: Merge all entity-level values into a single family balance sheet view.
        """
        total = liquid_assets + trust_assets + insurance_cash_value + private_placements
        
        # Calculate diversification mix
        liquid_pct = (liquid_assets / total) * 100 if total > 0 else 0
        alternative_pct = ((private_placements + insurance_cash_value) / total) * 100 if total > 0 else 0
        
        logger.info(f"UHNW_LOG: Unified Net Worth calculated: ${total:,.2f} ({alternative_pct:.1f}% Alternative)")
        
        return {
            "total_net_worth": round(total, 2),
            "liquidity_score": round(float(liquid_pct), 2),
            "alternative_exposure_pct": round(float(alternative_pct), 2),
            "status": "QUALIFIED_PURCHASER" if total >= 5000000 else "RETAIL_WEALTH"
        }
