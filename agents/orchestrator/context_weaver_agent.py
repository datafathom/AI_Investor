import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider

logger = logging.getLogger(__name__)

class ContextWeaverAgent(BaseAgent):
    """
    Agent 1.6: The Context Weaver
    
    Maintains Redis-based session memory for LLM prompts.
    
    Acceptance Criteria:
    - Injects relevant context (last 5 actions) into 100% of departmental role-switches
    """

    def __init__(self) -> None:
        super().__init__(name="orchestrator.context_weaver", provider=ModelProvider.GEMINI)
        self.context_buffer: List[Dict[str, Any]] = []
        self.max_context_items: int = 5

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Manage context for agent interactions."""
        event_type = event.get("type", "")
        
        if event_type == "action.completed":
            return self._record_action(event)
        elif event_type == "context.request":
            return self._provide_context(event)
        elif event_type == "role.switch":
            return self._inject_context_for_switch(event)
        
        return None

    def _record_action(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Record a completed action to the context buffer."""
        action = {
            "agent_id": event.get("agent_id", "unknown"),
            "action": event.get("action", ""),
            "result": event.get("result", ""),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
        self.context_buffer.append(action)
        
        # Keep only the last N items
        if len(self.context_buffer) > self.max_context_items:
            self.context_buffer = self.context_buffer[-self.max_context_items:]
        
        return {"status": "recorded", "buffer_size": len(self.context_buffer)}

    def _provide_context(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Provide the current context buffer."""
        return {
            "status": "context_provided",
            "context": self.context_buffer.copy(),
            "item_count": len(self.context_buffer),
        }

    def _inject_context_for_switch(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Inject context when switching to a different department role."""
        target_department = event.get("target_department", "")
        
        # Format context for LLM injection
        context_text = "\n".join([
            f"- [{c['timestamp']}] {c['agent_id']}: {c['action']} -> {c['result']}"
            for c in self.context_buffer
        ])
        
        logger.info(f"Context injected for switch to {target_department}")
        
        return {
            "status": "context_injected",
            "target_department": target_department,
            "context_items": len(self.context_buffer),
            "context_text": context_text,
        }
