"""
Threshold Monitor Service.
Calculates the percentage drawdown of individual assets relative to their entry price.
"""
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ThresholdMonitor:
    """
    Service for measuring asset-level drawdown.
    """

    @staticmethod
    def calculate_drawdown_pct(entry_price: Decimal, current_price: Decimal, side: str) -> float:
        """
        Calculate % loss from entry.
        :return: float (e.g., 0.10 for 10% loss)
        """
        if entry_price == 0:
            return 0.0

        if side.upper() == "LONG":
            # Loss if price < entry
            drawdown = (entry_price - current_price) / entry_price
        else:
            # SHORT: Loss if price > entry
            drawdown = (current_price - entry_price) / entry_price

        # We only care about losses (drawdowns)
        return float(round(max(Decimal("0"), drawdown), 4))

    @staticmethod
    def is_threshold_breached(drawdown_pct: float, threshold: float = 0.10) -> bool:
        """
        Check if the 10% (or custom) threshold is hit.
        """
        return drawdown_pct >= threshold
