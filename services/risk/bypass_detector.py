"""
Bypass Detector Service.
Audits incoming order requests to ensure they have been passed through the PositionSizer.
Prevents manual or rogue agent over-leveraging.
"""
import logging
from typing import Dict, Any, Tuple
from decimal import Decimal

logger = logging.getLogger(__name__)

class BypassDetector:
    """
    Validates that order metadata contains required risk certification.
    """

    @staticmethod
    def inspect_order(order_request: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify that the order has been properly sized.
        
        :param order_request: The full order payload
        :return: (is_approved, reason)
        """
        # institutional requirement: every order must have a 'risk_certified' timestamp
        if not order_request.get("risk_certified"):
            logger.critical(f"UNAUTHORIZED ORDER DETECTED: Order for {order_request.get('symbol')} lacks risk certification!")
            return False, "SECURITY_VIOLATION: Order bypassed PositionSizer logic."

        # Verify lot size isn't suspiciously round (e.g., exactly 10.0 lots usually suggests manual entry)
        lots = order_request.get("lots", 0)
        if lots > 0 and lots % 1.0 == 0:
            logger.warning(f"SUSPICIOUS_LOT_SIZE: Order for {lots} lots detected. Auditing calculation.")
            
        return True, "CERTIFIED"

    @staticmethod
    def log_bypass_attempt(symbol: str, requested_lots: float, agent_id: str):
        """
        Log a violation to the security audit trail.
        """
        # In a real system, this would trigger an alert to the user's mobile device
        # and lock the trading account.
        print(f"🚨 ALERT: Agent {agent_id} attempted to bypass risk controls for {requested_lots} lots of {symbol}!")
