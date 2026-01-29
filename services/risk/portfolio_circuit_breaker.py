"""
Portfolio Circuit Breaker Service.
Enforces the 3% daily drawdown freeze (Zen Mode).
All execution gateways must check this service before processing new entries.
"""
import logging
from typing import Dict, Any, Tuple
from services.risk.drawdown_aggregator import DrawdownAggregator

logger = logging.getLogger(__name__)

class PortfolioCircuitBreaker:
    """
    Guardian of the "Zen Mode" state.
    """

    def __init__(self, aggregator: DrawdownAggregator):
        self.aggregator = aggregator
        self.forced_lock = False

    def is_trading_allowed(self) -> Tuple[bool, str]:
        """
        Main check for the execution gateway.
        :return: (is_allowed, reason)
        """
        if self.forced_lock:
             return False, "ZEN_MODE: Manual administrative lock active."

        if self.aggregator.is_3_percent_breached():
            logger.warning("ZEN_MODE_ACTUAL: Daily drawdown exceeds 3%. Trading frozen.")
            return False, "ZEN_MODE: Daily 3% drawdown limit hit. Preservation protocol active."

        return True, "SYSTEM_READY"

    def set_administrative_lock(self, locked: bool):
        """
        Allows the Warden to manually freeze the system.
        """
        self.forced_lock = locked
        state = "LOCKED" if locked else "UNLOCKED"
        logger.info(f"CIRCUIT_BREAKER_OVERRIDE: System is now {state}.")
