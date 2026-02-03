"""
==============================================================================
FILE: services/ai/anthropic_client.py
ROLE: AI Model Client
PURPOSE: Interfaces with Anthropic Claude API (or Mock) for multi-persona 
         debate simulations (Bull vs. Bear).
         
INTEGRATION POINTS:
    - APIGovernor: Manages Anthropic rate limits (if live).
    - DebateChamberAgent: Primary consumer for debate orchestration.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import random
from typing import Optional

logger = logging.getLogger(__name__)

class AnthropicClient:
    """
    Client for Anthropic Claude API.
    Currently defaults to MOCK MODE as per Phase 9 requirements.
    """
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # If live, we would initialize the Anthropic SDK client here

    async def generate_persona_response(self, persona: str, topic: str, context: str = "") -> str:
        """
        Generates a response from a specific persona (Bull, Bear, Moderator).
        """
        _ = context  # Unused in mock mode
        if self.mock:
            # Simulate network latency for realism
            await asyncio.sleep(1.5)
            return self._generate_mock_reasoning(persona, topic)

        # Placeholder for real API call
        return "Live Anthropic API not implemented yet."

    def _generate_mock_reasoning(self, persona: str, topic: str) -> str:
        """
        Returns a canned response based on persona and topic.
        """
        from agents.prompt_loader import get_prompt_loader
        loader = get_prompt_loader()
        
        topic = topic.upper()
        persona_key = persona.lower()
        
        # Load from the DebateChamberAgent group in JSON
        prompt = loader.get_prompt("DebateChamberAgent", persona_key, {"topic": topic})
        
        if "PROMPT_NOT_FOUND" in prompt:
            return f"No opinion on {topic} for persona {persona}"
            
        return prompt

class AnthropicClientSingleton:
    """Singleton wrapper for AnthropicClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> AnthropicClient:
        """Returns the singleton instance of AnthropicClient."""
        if cls._instance is None:
            cls._instance = AnthropicClient(mock=mock)
        return cls._instance

def get_anthropic_client(mock: bool = True) -> AnthropicClient:
    """Legacy helper to get the anthropic client instance."""
    return AnthropicClientSingleton.get_instance(mock=mock)
