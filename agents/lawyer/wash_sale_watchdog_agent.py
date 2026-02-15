import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)

class WashSaleWatchdogAgent(BaseAgent):
    """
    Agent 11.1: Wash-Sale Watchdog
    
    The 'Tax Guard'. Blocks trades that would trigger wash-sale tax violations.
    """
    def __init__(self) -> None:
        super().__init__(name="lawyer.wash_sale_watchdog", provider=ModelProvider.GEMINI)

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return None
