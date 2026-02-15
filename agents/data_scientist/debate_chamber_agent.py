"""
==============================================================================
FILE: agents/debate_chamber_agent.py
ROLE: Agent Orchestrator
PURPOSE: Orchestrates multi-persona debates (Bull vs. Bear) using LLMs.
         Synthesizes a final consensus score.
         
INTEGRATION POINTS:
    - AnthropicClient: Generates persona responses.
    - AIStore/DebateStore: Frontend state.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import random
from typing import Dict, Any
from services.ai.anthropic_client import get_anthropic_client

logger = logging.getLogger(__name__)

class DebateChamberAgent:
    """
    Orchestrates a debate between multiple AI personas.
    """
    def __init__(self, mock: bool = True):
        self.client = get_anthropic_client(mock=mock)
        self.mock = mock
        self.transcript = []
        self.consensus = {}

    async def conduct_debate(self, ticker: str) -> Dict[str, Any]:
        """
        Runs a full debate cycle:
        1. Bull Argument
        2. Bear Argument
        3. Consensus/Synthesis
        """
        logger.info("Starting debate for %s", ticker)
        # 1. Bull Thesis
        bull_response = await self.client.generate_persona_response("BULL", ticker)
        self.transcript.append({"persona": "The Bull", "reasoning": bull_response, "role": "Proponent"})

        # 2. Bear Thesis
        bear_response = await self.client.generate_persona_response("BEAR", ticker)
        self.transcript.append({"persona": "The Bear", "reasoning": bear_response, "role": "Opponent"})

        # 3. Consensus (Moderator)
        consensus_response = await self.client.generate_persona_response("MODERATOR", ticker)
        
        # Calculate a simple "confidence score" (Mock logic)
        confidence = random.randint(40, 90)
        verdict = "BUY" if confidence > 65 else ("SELL" if confidence < 45 else "HOLD")
        
        self.consensus = {
            "decision": verdict,
            "score": confidence,
            "buy_ratio": confidence / 100.0,
            "is_approved": verdict == "BUY",
            "avg_score": confidence / 10.0
        }
        
        return {
            "ticker": ticker,
            "transcript": self.transcript,
            "consensus": self.consensus
        }

class DebateChamberAgentSingleton:
    """Singleton wrapper for DebateChamberAgent."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> DebateChamberAgent:
        """Returns the singleton instance of DebateChamberAgent."""
        if cls._instance is None:
            cls._instance = DebateChamberAgent(mock=mock)
        return cls._instance

def get_debate_agent(mock: bool = True) -> DebateChamberAgent:
    """Legacy helper to get the debate agent instance."""
    return DebateChamberAgentSingleton.get_instance(mock=mock)
