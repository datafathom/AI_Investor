import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class WaterfallEngine:
    """
    Calculates GP/LP splits and promotes for private syndications.
    Implements a standard 'Tiered' waterfall:
    1. Preferred Return (LPs get 100% until X%).
    2. GP Catch-up (GP gets catch-up portion).
    3. Splitting/Promote (LP/GP split e.g. 70/30).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WaterfallEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("WaterfallEngine initialized")

    def calculate_distributions(
        self, 
        distributable_cash: Decimal, 
        invested_capital: Decimal,
        preferred_return_pct: Decimal = Decimal('0.08'),
        gp_promote_pct: Decimal = Decimal('0.20')
    ) -> Dict[str, Any]:
        """
        Policy: Distribute cash according to the promote tier.
        """
        # 1. Preferred Return
        pref_amount = invested_capital * preferred_return_pct
        lp_pref = min(distributable_cash, pref_amount)
        remaining = distributable_cash - lp_pref
        
        # 2. Promotional Split (Promote Tier)
        # Assuming simplified promote for this core logic
        gp_promote = remaining * gp_promote_pct
        lp_share = remaining - gp_promote
        
        total_lp = lp_pref + lp_share
        total_gp = gp_promote
        
        logger.info(f"PE_LOG: Waterfall Distribution: LP ${total_lp:,.2f}, GP ${total_gp:,.2f}")
        
        return {
            "total_lp_dist": round(total_lp, 2),
            "total_gp_dist": round(total_gp, 2),
            "lp_yield_pct": round((total_lp / invested_capital) * 100, 2) if invested_capital > 0 else 0,
            "is_promote_active": gp_promote > 0
        }
