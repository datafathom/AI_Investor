"""
==============================================================================
FILE: agents/base_agent.py
ROLE: Abstract Base Class
PURPOSE: Defines the interface and core logic (start/stop/health) for all agents.
USAGE: Inherit from BaseAgent and implement process_event(event).
INPUT/OUTPUT:
    - Input: Dict[str, Any] (Kafka/Event payload)
    - Output: Optional[Dict[str, Any]] (Response or action)
==============================================================================
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


from services.system.model_manager import get_model_manager, ModelProvider, ModelConfig

class BaseAgent(ABC):
    """
    Abstract base class for all AI Investor agents.
    
    Attributes:
        name (str): Unique identifier for the agent.
        is_active (bool): Whether the agent is currently processing events.
        model_config (ModelConfig): The preferred LLM configuration for this agent.
    """
    
    def __init__(self, name: str, provider: ModelProvider = ModelProvider.GEMINI) -> None:
        """
        Initialize the base agent.
        
        Args:
            name: Unique identifier for this agent instance.
            provider: The preferred LLM provider (defaults to Gemini/Free-tier).
        """
        self.name = name
        self.is_active = False
        self.model_manager = get_model_manager()
        
        # Default model assignment (Agnostic setup)
        model_map = {
            ModelProvider.OPENAI: "gpt-4o",
            ModelProvider.ANTHROPIC: "claude-3-5-sonnet-20240620",
            ModelProvider.GEMINI: "gemini-1.5-flash",
            ModelProvider.PERPLEXITY: "llama-3-sonar-large-32k-online"
        }
        
        self.model_config = ModelConfig(
            provider=provider,
            model_id=model_map.get(provider, "mock-model")
        )
        
        logger.info(f"Agent '{self.name}' initialized with {provider.value} ({self.model_config.model_id})")
    
    async def get_completion(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        LLM Agnostic completion interface for agents.
        Usage: response = await self.get_completion("Analyze this trade...")
        """
        sys_msg = system_message or f"You are the {self.name} agent in the AI Investor platform."
        return await self.model_manager.get_completion(
            prompt=prompt,
            config=self.model_config,
            system_message=sys_msg
        )

    @abstractmethod
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process an incoming event from the Kafka stream.
        
        Args:
            event: The event payload to process.
            
        Returns:
            Optional response/action to take, or None if no action needed.
        """
        pass
    
    def start(self) -> None:
        """Activate the agent for event processing."""
        self.is_active = True
        logger.info(f"Agent '{self.name}' started")
    
    def stop(self) -> None:
        """Deactivate the agent."""
        self.is_active = False
        logger.info(f"Agent '{self.name}' stopped")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Return the agent's current health status.
        Used by the Watchdog/Heartbeat monitor.
        """
        return {
            'agent': self.name,
            'active': self.is_active,
            'status': 'healthy' if self.is_active else 'inactive'
        }
