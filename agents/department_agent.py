from typing import Any, Dict, Optional
import logging
from agents.base_agent import BaseAgent
from services.infrastructure.event_bus import EventBusService

logger = logging.getLogger(__name__)

class DepartmentAgent(BaseAgent):
    """
    A specialized agent belonging to a specific department.
    Handles department-specific events and metrics updates.
    """
    
    def __init__(self, name: str, dept_id: int, role: str) -> None:
        super().__init__(name=name)
        self.dept_id = dept_id
        self.role = role
        self.event_bus = EventBusService()
        logger.info(f"DepartmentAgent '{self.name}' (Dept {self.dept_id}) initialized as '{self.role}'")

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process department events.
        """
        if not self.is_active:
            return None
            
        logger.info(f"Agent {self.name} processing event: {event.get('type')}")
        
        # Logic to handle specific department event types
        # For now, we simulate processing and return a telemetry update
        return {
            "type": "agent_telemetry",
            "agent_id": self.name,
            "dept_id": self.dept_id,
            "status": "busy",
            "message": f"Processed {event.get('type')}"
        }

    def _load_prompt(self, filename: str) -> str:
        """Load a prompt template from the agents/prompts directory."""
        import os
        # Base path relative to project root (assuming cwd is project root)
        path = os.path.join("agents", "prompts", filename)
        if not os.path.exists(path):
            logger.warning(f"Prompt file not found: {path}, using fallback.")
            return ""
        with open(path, "r") as f:
            return f.read()

    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Directly invoke the agent for a specialized task.
        """
        logger.info(f"Invoking agent {self.name} with payload: {payload}")
        
        # 1. Load Templates
        sys_tmpl = self._load_prompt("department_agent_system.txt")
        user_tmpl = self._load_prompt("department_agent_user.txt")

        # Fallbacks if file read fails
        if not sys_tmpl:
            sys_tmpl = "You are {agent_name}. Role: {role}."
        if not user_tmpl:
            user_tmpl = "Task: {action}. Context: {context}"

        # 2. Format Prompts
        system_prompt = sys_tmpl.format(
            agent_name=self.name.replace('_', ' ').title(),
            dept_id=self.dept_id,
            role=self.role
        )

        action = payload.get('action', 'general_query')
        data = payload.get('data', {})
        
        user_prompt = user_tmpl.format(
            action=action,
            context=data
        )

        try:
            # 3. Call LLM (Agnostic)
            response = await self.get_completion(prompt=user_prompt, system_message=system_prompt)
            
            result = {
                "agent": self.name,
                "status": "success",
                "response": response,
                "metadata": {
                    "role": self.role,
                    "model": self.model_config.model_id
                }
            }
            
            # 4. Broadcast Event (Simulate work done)
            self.event_bus.publish(f"dept.{self.dept_id}.agents", result)
            
            return result
            
        except Exception as e:
            logger.error(f"Agent {self.name} failed during LLM invocation: {e}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e)
            }
