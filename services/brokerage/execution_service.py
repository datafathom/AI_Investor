
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
from services.brokerage.brokerage_service import get_brokerage_service
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class ExecutionService:
    """
    Core engine for routing and managing live orders.
    Integrates with security safeties and brokerage APIs.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExecutionService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._brokerage = get_brokerage_service()
        self._is_frozen = False # Internal state for kill switch cache if needed

    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes and routes an order.
        Perform Pre-Flight Safety Checks.
        """
        symbol = order_data.get('symbol')
        qty = order_data.get('qty', 0)
        side = order_data.get('side', 'buy').lower()
        order_type = order_data.get('type', 'market')

        # 1. Pre-Flight Check: Kill Switch
        if self._check_kill_switch():
            logger.critical(f"ORDER BLOCKED: Kill Switch is active. Symbol: {symbol}")
            return {"status": "REJECTED", "reason": "System Halted (Kill Switch)"}

        # 2. Pre-Flight Check: Risk Limits (Simulation)
        if not self._validate_risk_limits(order_data):
            logger.warning(f"ORDER BLOCKED: Risk limit exceeded. Symbol: {symbol}")
            return {"status": "REJECTED", "reason": "Risk Management Violation"}

        # 3. Routing to Brokerage
        logger.info(f"Routing {side} order for {qty} {symbol}...")
        
        if self._brokerage._is_simulated:
            return {
                "status": "FILLED",
                "order_id": f"sim_ord_{datetime.now().timestamp()}",
                "symbol": symbol,
                "qty": qty,
                "price": 150.00, # Mock price
                "timestamp": datetime.now().isoformat(),
                "simulated": True
            }

        try:
            # Alpaca client call
            alpaca_client = self._brokerage._client
            order = alpaca_client.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force='gtc'
            )
            return {
                "status": "SUBMITTED",
                "order_id": order.id,
                "symbol": symbol,
                "qty": int(order.qty),
                "timestamp": order.created_at.isoformat()
            }
        except Exception as e:
            logger.error(f"Execution Error for {symbol}: {e}")
            return {"status": "ERROR", "reason": str(e)}

    def _check_kill_switch(self) -> bool:
        """
        Checks if the system is currently halted.
        In a real app, this would check a global Redis key or DB flag.
        """
        # For simulation, we check the secret manager or a known flag
        return os.getenv('SYSTEM_HALTED') == 'TRUE'

    def _validate_risk_limits(self, order_data: Dict[str, Any]) -> bool:
        """
        Ensures the order doesn't violate core risk parameters.
        """
        qty = order_data.get('qty', 0)
        # Mock Logic: Reject any order with qty > 1000 for safety demo
        if qty > 1000:
            return False
        return True

def get_execution_service():
    return ExecutionService()
