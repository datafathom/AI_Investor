"""
Protector Agent (The Warden).
Final gatekeeper for all trades. Enforces risk protocols.
"""
from typing import Dict, Any, Optional
import logging
from agents.base_agent import BaseAgent
from services.risk_manager import RiskManager
from services.warden.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class ProtectorAgent(BaseAgent):
    """
    The Protector Agent (Warden).
    Enforces the 'Prime Directive' of capital preservation.
    """
    
    def __init__(self):
        super().__init__(name='ProtectorAgent')
        self.risk_manager = RiskManager()
        self.circuit_breaker = CircuitBreaker()
        
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process order validation requests.
        """
        event_type = event.get('type')
        
        if event_type == 'VALIDATE_ORDER':
            return self._validate_order(event)
            
        return None

    def _validate_order(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an order against risk rules.
        """
        amount = event.get('amount', 0.0)
        balance = event.get('balance', 100000.0)
        daily_loss = event.get('daily_loss', 0.0)
        
        # 1. Check Circuit Breaker
        if self.circuit_breaker.check_circuit(balance, daily_loss):
            return {
                "action": "REJECT",
                "reason": "CIRCUIT_BREAKER_TRIPPED"
            }
            
        # 2. Check 1% Rule
        if not self.risk_manager.check_trade_risk(balance, amount):
            return {
                "action": "REJECT",
                "reason": "RISK_EXCEEDS_1_PERCENT"
            }
            
        return {
            "action": "APPROVE",
            "reason": "WITHIN_RISK_LIMITS"
        }
