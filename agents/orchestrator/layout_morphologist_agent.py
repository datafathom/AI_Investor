import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)

class LayoutMorphologistAgent(BaseAgent):
    """
    Agent 1.4: The Layout Morphologist
    
    Predictive UI management based on context and events.
    
    Acceptance Criteria:
    - Auto-transition to Trader HUD within 500ms of high-volatility event detection
    """

    def __init__(self) -> None:
        super().__init__(name="orchestrator.layout_morphologist", provider=ModelProvider.GEMINI)
        self.current_layout: str = "mission_control"
        self.volatility_threshold: float = 0.02

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process events and trigger layout transitions."""
        event_type = event.get("type", "")
        
        if event_type == "market.volatility":
            return self._check_volatility_trigger(event)
        elif event_type == "layout.switch":
            return self._switch_layout(event)
        
        return None

    def _check_volatility_trigger(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if volatility warrants a layout transition."""
        volatility = event.get("volatility", 0.0)
        
        if abs(volatility) > self.volatility_threshold:
            logger.info(f"High volatility detected ({volatility:.2%}), switching to Trader HUD")
            return self._switch_layout({"target": "trader_hud", "reason": "volatility_spike"})
        
        return None

    def _switch_layout(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Switch the UI layout."""
        target = event.get("target", "mission_control")
        reason = event.get("reason", "user_request")
        
        previous = self.current_layout
        self.current_layout = target
        
        return {
            "status": "layout_switched",
            "from": previous,
            "to": target,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
