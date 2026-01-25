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
        topic = topic.upper()
        
        if persona == "BULL":
            responses = [
                f"The fundamentals for {topic} are incredibly strong. Revenue growth is "
                "accelerating, and their AI moat is widening.",
                f"Market sentiment for {topic} is shifting positive. The technicals show a "
                "clear breakout pattern forming on the weekly chart.",
                f"{topic} is undervalued relative to its peers. The forward P/E suggests "
                "significant upside potential as margins expand.",
                f"Institutional accumulation of {topic} has been heavy. Smart money is "
                "positioning for the next leg up."
            ]
            return random.choice(responses)
            
        elif persona == "BEAR":
            responses = [
                f"{topic} is significantly overextended here. The RSI is flashing overbought, "
                "and a correction is imminent.",
                f"Macro headwinds are going to crush {topic}'s guidance. Inflationary "
                "pressures are eating into their margins.",
                f"The valuation for {topic} is completely detached from reality. This is a "
                "classic bubble formation.",
                f"Insider selling at {topic} has been rampant. Management knows the peak is in."
            ]
            return random.choice(responses)
            
        elif persona == "MODERATOR":
            return (f"Let's bring this to a conclusion. We've heard compelling arguments for both "
                    f"sides of {topic}. Based on the volatility and volume, caution is advised, "
                    "but the trend remains the deciding factor.")

        return "I have no opinion on this matter."

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
