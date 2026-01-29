"""
Zone Mitigation Tracker.
Determines when a previously identified liquidity zone has been neutralized.
"""
import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ZoneMitigation:
    """
    Logic for neutralizing logic zones.
    """

    @staticmethod
    def check_mitigation(zone: Dict[str, Any], current_price: float) -> bool:
        """
        Identify if price has entered and exited (or breached) a zone.
        
        Logic for primary mitigation:
        - For DEMAND: If price falls below zone_low.
        - For SUPPLY: If price rises above zone_high.
        """
        price = Decimal(str(current_price))
        zone_low = Decimal(str(zone.get("price_low")))
        zone_high = Decimal(str(zone.get("price_high")))
        z_type = zone.get("type", "").upper()

        if z_type == "DEMAND":
            if price < zone_low:
                return True
        elif z_type == "SUPPLY":
            if price > zone_high:
                return True

        return False
