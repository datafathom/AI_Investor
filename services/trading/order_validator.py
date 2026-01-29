"""
Order Validator Service.
Ensures trade requests meet institutional quality standards before execution.
Mandates Stop Loss parameters.
"""
import logging
from typing import Dict, Any, Tuple
from decimal import Decimal

logger = logging.getLogger(__name__)

class OrderValidator:
    """
    Final gate before brokerage submission.
    """

    @staticmethod
    def validate_submission(order_request: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Final check for required fields.
        """
        # 1. Mandatory SL Check
        sl = order_request.get("stop_loss")
        if sl is None or float(sl) <= 0:
            logger.error(f"VAL_FAIL: Order for {order_request.get('symbol')} missing Stop Loss!")
            return False, "REJECTED: Mandatory Stop Loss is missing or invalid."

        # 2. Symbol Validation
        if not order_request.get("symbol"):
            return False, "REJECTED: Symbol is required."

        # 3. Side Validation
        if order_request.get("side", "").upper() not in ["LONG", "SHORT"]:
            return False, "REJECTED: Invalid side. Must be LONG or SHORT."

        return True, "READY_FOR_EXECUTION"
