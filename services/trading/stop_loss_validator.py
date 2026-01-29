import logging
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)

class StopLossValidatorService:
    """
    Validates that every trade request includes a valid stop-loss parameter.
    Blocks orders that violate the 'no unprotected positions' rule.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StopLossValidatorService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("StopLossValidatorService initialized")

    def validate_stop_loss(
        self, 
        direction: str, 
        entry_price: Decimal, 
        stop_loss: Optional[Decimal]
    ) -> bool:
        """
        Validate that a stop-loss is present and correctly positioned.
        
        Rules:
        - LONG: stop_loss must be < entry_price
        - SHORT: stop_loss must be > entry_price
        - Stop-loss cannot be None
        """
        if stop_loss is None:
            logger.error("BLOCKED: Trade submitted without stop-loss")
            return False
            
        if direction == "LONG" and stop_loss >= entry_price:
            logger.error(f"BLOCKED: LONG stop-loss {stop_loss} >= entry {entry_price}")
            return False
            
        if direction == "SHORT" and stop_loss <= entry_price:
            logger.error(f"BLOCKED: SHORT stop-loss {stop_loss} <= entry {entry_price}")
            return False
            
        logger.info(f"VALID: Stop-loss {stop_loss} approved for {direction} @ {entry_price}")
        return True

    def calculate_max_risk_distance(
        self, 
        entry_price: Decimal, 
        account_balance: Decimal, 
        risk_percent: Decimal = Decimal("0.01")
    ) -> Decimal:
        """
        Calculate the maximum stop-loss distance based on 1% risk rule.
        """
        max_risk_amount = account_balance * risk_percent
        # This is simplified; in practice, you'd need lot size, pip value, etc.
        return max_risk_amount
