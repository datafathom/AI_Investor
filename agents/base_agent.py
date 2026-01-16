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


class BaseAgent(ABC):
    """
    Abstract base class for all AI Investor agents.
    
    Attributes:
        name (str): Unique identifier for the agent.
        is_active (bool): Whether the agent is currently processing events.
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize the base agent.
        
        Args:
            name: Unique identifier for this agent instance.
        """
        self.name = name
        self.is_active = False
        logger.info(f"Agent '{self.name}' initialized")
    
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
