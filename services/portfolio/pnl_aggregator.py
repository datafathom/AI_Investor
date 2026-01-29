"""
Unrealized P&L Aggregator.
Calculates real-time PnL for all open positions using the live FX stream.
"""
import logging
from decimal import Decimal
from typing import Dict, List, Any
from datetime import datetime

from services.pip_calculator import PipCalculatorService
from services.portfolio.fast_balance import get_balance_service

logger = logging.getLogger(__name__)

class PnLAggregator:
    """
    Service for calculating portfolio-wide unrealized gains/losses.
    """
    
    def __init__(self):
        self.pip_calc = PipCalculatorService()
        self.balance_svc = get_balance_service()

    def calculate_position_pnl(self, position: Dict[str, Any], current_price: float) -> Decimal:
        """
        Calculate PnL for a single position.
        
        :param position: Dict with 'symbol', 'entry_price', 'side' (LONG/SHORT), 'lots'
        :param current_price: Current market price
        :return: Decimal PnL in USD
        """
        side = position.get("side", "LONG").upper()
        entry_price = Decimal(str(position.get("entry_price")))
        curr_price = Decimal(str(current_price))
        lots = Decimal(str(position.get("lots", 0)))
        
        # Calculate pip difference
        pips = self.pip_calc.calculate_pips(entry_price, curr_price, position["symbol"])
        if side == "SHORT":
            pips = -pips
            
        # Standard Pip Value = $10.00 for standard lot (approx)
        pip_v = Decimal("10.00") if not position["symbol"].endswith("JPY") else Decimal("7.00")
        
        pnl = Decimal(str(pips)) * pip_v * lots
        return pnl

    def aggregate_total_pnl(self, open_positions: List[Dict[str, Any]], spot_prices: Dict[str, float]) -> Decimal:
        """
        Sum PnL across all open positions.
        """
        total_pnl = Decimal("0.00")
        for pos in open_positions:
            symbol = pos["symbol"]
            if symbol in spot_prices:
                total_pnl += self.calculate_position_pnl(pos, spot_prices[symbol])
        
        return total_pnl
