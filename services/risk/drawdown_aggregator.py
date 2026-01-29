"""
Drawdown Aggregator Service.
Tracks aggregate system-wide daily P&L to calculate global portfolio drawdown.
"""
import logging
from decimal import Decimal
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DrawdownAggregator:
    """
    Calculates total daily drawdown percentage across all accounts.
    """

    def __init__(self, start_of_day_equity: Decimal = Decimal("100000.00")):
        self.start_equity = start_of_day_equity
        self.current_realized_pnl = Decimal("0.00")
        self.current_unrealized_pnl = Decimal("0.00")

    def update_pnl(self, realized: Decimal, unrealized: Decimal):
        """
        Update the running P&L totals for the current session.
        """
        self.current_realized_pnl = realized
        self.current_unrealized_pnl = unrealized

    def get_total_drawdown_pct(self) -> float:
        """
        Return the current % loss from the start of the day.
        :return: float (e.g., 0.03 for 3% loss)
        """
        current_equity = self.start_equity + self.current_realized_pnl + self.current_unrealized_pnl
        
        if self.start_equity <= 0:
            return 0.0

        drawdown = (self.start_equity - current_equity) / self.start_equity
        
        # Return max of 0 and drawdown (we only care about losses)
        return float(round(max(Decimal("0"), drawdown), 4))

    def is_3_percent_breached(self) -> bool:
        """
        The global institutional circuit breaker threshold.
        """
        return self.get_total_drawdown_pct() >= 0.03
