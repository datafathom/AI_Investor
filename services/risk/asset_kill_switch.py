"""
Asset Kill Switch Service.
The 'Nuclear Option' for individual assets.
Triggers immediate full liquidation if an asset loses 10% from entry.
"""
import logging
from decimal import Decimal
from typing import Dict, List, Any

from services.risk.threshold_monitor import ThresholdMonitor

logger = logging.getLogger(__name__)

class AssetKillSwitch:
    """
    Guardian service that enforces the 10% individual asset loss limit.
    """

    def __init__(self, kill_threshold: float = 0.10):
        self.monitor = ThresholdMonitor()
        self.kill_threshold = kill_threshold
        self.interventions = 0

    def inspect_portfolio(self, open_positions: List[Dict[str, Any]], spot_prices: Dict[str, float]) -> List[str]:
        """
        Scan all open positions for 10% violations.
        :return: List of asset symbols to liquidate immediately.
        """
        to_liquidate = []

        for pos in open_positions:
            symbol = pos["symbol"]
            if symbol not in spot_prices:
                continue

            entry = Decimal(str(pos["entry_price"]))
            current = Decimal(str(spot_prices[symbol]))
            side = pos["side"]

            drawdown = self.monitor.calculate_drawdown_pct(entry, current, side)
            
            if drawdown >= self.kill_threshold:
                logger.critical(f"NUCLEAR_KILL: {symbol} hit {drawdown:.2%} drawdown (Max: {self.kill_threshold:.2%}).")
                to_liquidate.append(symbol)
                self.interventions += 1

        return to_liquidate

    def execute_liquidation(self, symbol: str):
        """
        MOCK: Send immediate 'FULL_CLOSE' command to the broker.
        """
        print(f"☢️ NUCLEAR_ACTION: Liquidating all {symbol} positions immediately.")
