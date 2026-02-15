import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)

class TrafficControllerAgent(BaseAgent):
    """
    Agent 1.3: The Traffic Controller
    
    Manages Kafka backpressure and message routing.
    
    Acceptance Criteria:
    - Consumer lag for `market.live` topic remains < 200ms during 5k msg/sec spikes
    """

    def __init__(self) -> None:
        super().__init__(name="orchestrator.traffic_controller", provider=ModelProvider.GEMINI)
        self.current_lag_ms: float = 0.0
        self.message_rate: float = 0.0
        self.backpressure_active: bool = False

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Monitor Kafka metrics and apply backpressure if needed."""
        event_type = event.get("type", "")
        
        if event_type == "kafka.metrics":
            return self._process_metrics(event)
        elif event_type == "backpressure.check":
            return self._check_backpressure()
        
        return None

    def _process_metrics(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process Kafka consumer metrics."""
        self.current_lag_ms = event.get("consumer_lag_ms", 0.0)
        self.message_rate = event.get("messages_per_sec", 0.0)
        
        # Apply backpressure if lag exceeds threshold
        lag_threshold_ms = 200.0
        if self.current_lag_ms > lag_threshold_ms and not self.backpressure_active:
            self.backpressure_active = True
            logger.warning(
                f"Backpressure ACTIVATED: Lag={self.current_lag_ms}ms > {lag_threshold_ms}ms"
            )
        elif self.current_lag_ms <= lag_threshold_ms and self.backpressure_active:
            self.backpressure_active = False
            logger.info("Backpressure RELEASED: Lag normalized")
        
        return {
            "status": "metrics_processed",
            "lag_ms": self.current_lag_ms,
            "rate_per_sec": self.message_rate,
            "backpressure": self.backpressure_active,
        }

    def _check_backpressure(self) -> Dict[str, Any]:
        """Return current backpressure status."""
        return {
            "backpressure_active": self.backpressure_active,
            "current_lag_ms": self.current_lag_ms,
            "meets_sla": self.current_lag_ms < 200.0,
        }
