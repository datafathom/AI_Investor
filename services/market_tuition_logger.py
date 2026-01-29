"""
Market Tuition Logger Service.
Logs demo losses as 'tuition' lessons.
"""
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class MarketTuitionLoggerService:
    def log_loss(self, trade_id: str, amount: Decimal, reason: str, agent_id: str = "system"):
        """
        Log a realized loss in demo mode as tuition.
        """
        log_entry = {
            "event": "MARKET_TUITION",
            "trade_id": trade_id,
            "loss_amount": float(amount),
            "lesson": reason,
            "agent": agent_id
        }
        # In a real impl, this would write to DB
        logger.info(f"🎓 Market Tuition Paid: ${amount} | Lesson: {reason} | Trade: {trade_id}")
        return log_entry
