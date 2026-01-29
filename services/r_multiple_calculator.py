"""
R-Multiple Calculation Service.
Measures reward-to-risk ratio for performance analysis.
"""
from decimal import Decimal
from typing import Optional

class RMultipleCalculator:
    """
    Calculates the R-Multiple for a trade.
    R-Multiple = (Revenue - Entry) / (Initial Risk)
    """

    @staticmethod
    def calculate(
        entry_price: float,
        exit_price: float,
        stop_loss: float,
        direction: str
    ) -> float:
        """
        Calculate R-Multiple.
        
        Args:
            entry_price: Execution price at entry.
            exit_price: Execution price at exit.
            stop_loss: Initial stop loss level.
            direction: 'LONG' or 'SHORT'.
            
        Returns:
            float: The R-Multiple (e.g., 2.0 for 2R profit, -1.0 for full stop loss hit).
        """
        entry = Decimal(str(entry_price))
        exit_p = Decimal(str(exit_price))
        sl = Decimal(str(stop_loss))
        
        # Avoid division by zero
        if entry == sl:
            return 0.0
            
        if direction.upper() == 'LONG':
            # Revenue = Exit - Entry
            # Risk = Entry - StopLoss
            revenue = exit_p - entry
            risk = entry - sl
            if risk <= 0: return -1.0 # Invalid risk setup
            return float(revenue / risk)
            
        elif direction.upper() == 'SHORT':
            # Revenue = Entry - Exit
            # Risk = StopLoss - Entry
            revenue = entry - exit_p
            risk = sl - entry
            if risk <= 0: return -1.0
            return float(revenue / risk)
            
        return 0.0
