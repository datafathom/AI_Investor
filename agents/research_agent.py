"""
==============================================================================
FILE: agents/research_agent.py
ROLE: Agent Layer
PURPOSE: Manages research queries using Perplexity Client.
         Future: Could cache results or combine multiple queries.
==============================================================================
"""

import logging
from typing import Dict, Any
from services.ai.perplexity_client import get_perplexity_client

logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    Agent for conducting market research.
    """
    def __init__(self, mock: bool = True):
        self.client = get_perplexity_client(mock=mock)
        self.history = []

    async def ask(self, query: str) -> Dict[str, Any]:
        """
        Asks a question and returns the answer with citations.
        """
        logger.info("Researching: %s", query)
        result = await self.client.search(query)
        # Store in history (in-memory for now)
        self.history.append({
            "query": query,
            "answer": result["answer"],
            "citations": result["citations"]
        })
        return result

class ResearchAgentSingleton:
    """Singleton wrapper for ResearchAgent."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> ResearchAgent:
        """Returns the singleton instance of ResearchAgent."""
        if cls._instance is None:
            cls._instance = ResearchAgent(mock=mock)
        return cls._instance

def get_research_agent(mock: bool = True) -> ResearchAgent:
    """Legacy helper to get the research agent instance."""
    return ResearchAgentSingleton.get_instance(mock=mock)
