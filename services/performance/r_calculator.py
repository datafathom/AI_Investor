"""
R-Calculator Service.
Determines initial risk amounts at entry and R-multiples at exit.
R-Multiple = (Exit Price - Entry Price) / (Entry Price - Stop Loss Price)
"""
import logging
from decimal import Decimal
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class RCalculator:
    """
    Quantifies risk and performance using the R-Multiple framework.
    """

    @staticmethod
    def calculate_initial_risk(entry_price: Decimal, stop_loss_price: Decimal, lots: Decimal, symbol: str) -> Decimal:
        """
        Calculate total financial risk in USD at the moment of entry.
        """
        pip_v = Decimal("10.00") if not symbol.endswith("JPY") else Decimal("7.00")
        
        # Calculate pip distance to stop
        # Note: simplistic pip distance calc for R-purposes
        if symbol.endswith("JPY"):
            pip_dist = abs(entry_price - stop_loss_price) * 100
        else:
            pip_dist = abs(entry_price - stop_loss_price) * 10000
            
        risk_usd = pip_dist * pip_v * lots
        return risk_usd

    @staticmethod
    def calculate_r_multiple(pnl_usd: Decimal, initial_risk_usd: Decimal) -> float:
        """
        Normalize PnL against initial risk.
        :return: float R (e.g., 2.5, -1.0)
        """
        if initial_risk_usd == 0:
            return 0.0
        
        r_value = pnl_usd / initial_risk_usd
        return float(round(r_value, 2))

    @staticmethod
    def get_real_time_r(current_price: Decimal, entry_price: Decimal, stop_loss: Decimal, side: str) -> float:
        """
        Calculate floating R-multiple for an open position.
        """
        risk_distance = abs(entry_price - stop_loss)
        if risk_distance == 0:
            return 0.0
            
        profit_distance = (current_price - entry_price) if side.upper() == "LONG" else (entry_price - current_price)
        
        r_floating = profit_distance / risk_distance
        return float(round(r_floating, 2))
