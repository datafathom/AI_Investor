"""
Stop Loss Sentinel Service.
Monitors open positions against their hard stop-loss levels.
Triggers immediate liquidation on breach.
"""
import logging
from decimal import Decimal
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

from services.communication.notification_hub import notification_hub

class StopLossSentinel:
    """
    Autonomous protection service (The Sentinel).
    """

    def __init__(self):
        # In a real system, this would hold a high-priority Kafka producer
        self.triggered_count = 0

    async def check_position(self, position: Dict[str, Any], current_price: float) -> bool:
        """
        Verify if a position has breached its SL.
        
        :param position: Dict with 'symbol', 'side', 'stop_loss'
        :param current_price: Current market rate
        :return: True if trigger hit
        """
        side = position.get("side", "LONG").upper()
        stop_level = Decimal(str(position.get("stop_loss", 0)))
        price = Decimal(str(current_price))

        if side == "LONG":
            is_breached = price <= stop_level
        else:
            is_breached = price >= stop_level

        if is_breached:
            logger.critical(f"SENTINEL_TRIGGER: {position['symbol']} {side} level {stop_level} breached at {price}!")
            
            # Phase 30/31: Trigger real-time SMS/Email alert
            await notification_hub.broadcast_alert(
                title=f"SENTINEL BREACH: {position['symbol']}",
                message=f"Stop level {stop_level} breached at {price}. Liquidating position.",
                severity="CRITICAL"
            )
            
            self.triggered_count += 1
            return True

        return False

    def broadcast_kill(self, symbol: str, reason: str):
        """
        MOCK: Send event to emergency-kill topic.
        """
        print(f"📡 KAFKA: [emergency-kill] Action: CLOSE, Asset: {symbol}, Reason: {reason}")
