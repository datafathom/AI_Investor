"""
Strategy Zone Filter.
Hard filter for SearcherAgent to prevent low-probability trades into institutional zones.
Blocks 'Buy into Supply' and 'Sell into Demand'.
"""
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class ZoneFilter:
    """
    Compliance logic for liquidity-aware trading.
    """

    @staticmethod
    def validate_signal(
        side: str, 
        current_price: float, 
        nearest_supply: Dict[str, Any] = None, 
        nearest_demand: Dict[str, Any] = None
    ) -> Tuple[bool, str]:
        """
        Validate a trading signal against nearby logic zones.
        """
        side = side.upper()

        # 1. Check for Buy into Supply
        if side == "BUY" and nearest_supply:
            supply_low = float(nearest_supply.get("price_low"))
            # If price is within 5 pips of supply low, block buy
            if current_price >= (supply_low - 0.0005):
                return False, f"LIMIT_BLOCKED: Buying into institutional SUPPLY zone at {supply_low}."

        # 2. Check for Sell into Demand
        if side == "SELL" and nearest_demand:
            demand_high = float(nearest_demand.get("price_high"))
            # If price is within 5 pips of demand high, block sell
            if current_price <= (demand_high + 0.0005):
                return False, f"LIMIT_BLOCKED: Selling into institutional DEMAND zone at {demand_high}."

        return True, "SIGNAL_CLEARED"
