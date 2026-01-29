import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RestrictionEngine:
    """
    Enforces SEC Rule 144 volume restrictions for corporate insiders (Affiliates).
    Limits sales to Greater(1% of shares, Avg Weekly Volume).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RestrictionEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("RestrictionEngine initialized")

    def check_rule144_selling_limit(
        self, 
        shares_outstanding: int, 
        avg_weekly_volume_4wk: int
    ) -> Dict[str, Any]:
        """
        Policy: Max sell = Max(0.01 * outstanding, avg_weekly_volume).
        """
        one_pct_limit = int(shares_outstanding * 0.01)
        volume_limit = avg_weekly_volume_4wk
        
        max_allowed = max(one_pct_limit, volume_limit)
        
        logger.info(f"RULE144_LOG: Limit check. 1%={one_pct_limit:,}, Vol={volume_limit:,}. Allowed={max_allowed:,}")
        
        return {
            "one_percent_limit": one_pct_limit,
            "volume_limit": volume_limit,
            "max_quarterly_sale_qty": max_allowed,
            "restriction_basis": "SHARES_OUTSTANDING" if one_pct_limit > volume_limit else "ADTV"
        }
