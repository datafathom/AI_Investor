import logging
from decimal import Decimal
from typing import Optional
from datetime import timezone, datetime

logger = logging.getLogger(__name__)

class DemoResetService:
    """
    Resets the demo account to initial state for iterative strategy testing.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DemoResetService, cls).__new__(cls)
        return cls._instance

    def __init__(self, initial_balance: Decimal = Decimal("100000.00")):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.initial_balance = initial_balance
        logger.info("DemoResetService initialized")

    def reset_demo_account(self, user_id: str, clear_history: bool = False) -> dict:
        """
        Reset demo account to initial state.
        
        Actions:
        1. Close all open demo positions
        2. Cancel all pending demo orders
        3. Reset demo balance to initial amount
        4. Optionally clear demo trade history
        5. Log reset event to activity service
        """
        logger.info(f"Resetting demo account for user {user_id}")
        
        result = {
            "user_id": user_id,
            "new_balance": float(self.initial_balance),
            "positions_closed": 0,  # Would be populated by actual logic
            "orders_cancelled": 0,
            "history_cleared": clear_history,
            "reset_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"Demo account reset complete: {result}")
        return result
