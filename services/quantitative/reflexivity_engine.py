import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ReflexivityEngine:
    """
    Models 'Michael Green' style reflexivity and passive indexing bubble risk.
    Tracks 'Inelastic Market' behavior where flows dictate price more than fundamentals.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ReflexivityEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("ReflexivityEngine initialized")

    def check_passive_saturation(self, ticker: str, big_three_shares: int, total_outstanding: int) -> Dict[str, Any]:
        """
        Policy: Passive ownership > 40% creates extreme reflexivity risk.
        """
        passive_pct = Decimal(str(big_three_shares)) / Decimal(str(total_outstanding))
        is_saturated = passive_pct > Decimal('0.40')
        
        logger.info(f"REFLEX_LOG: {ticker} passive ownership: {passive_pct:.1%}. Saturated: {is_saturated}")
        
        return {
            "ticker": ticker,
            "passive_ownership_pct": round(Decimal(str(passive_pct * 100)), 2),
            "is_saturated_reflexive": is_saturated,
            "inelasticity_rank": "HIGH" if is_saturated else "LOW"
        }

    def simulate_inelastic_flow_impact(self, current_price: float, net_inflow_m: float, market_depth_coef: float = 0.2) -> float:
        """
        Simplified Inelastic Market model: Price change is non-linearly related to net index flows.
        """
        # Price change ~ (Flow / Deep Liquidity)
        price_impact = (net_inflow_m * market_depth_coef) / 100 # 100M flow moves price X %
        new_price = current_price * (1 + price_impact)
        return round(new_price, 2)
