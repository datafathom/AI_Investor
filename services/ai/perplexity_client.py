"""
==============================================================================
FILE: services/ai/perplexity_client.py
ROLE: AI Model Client
PURPOSE: Interfaces with Perplexity AI (Sonar) or Mock for real-time 
         citation-backed market research.
         
INTEGRATION POINTS:
    - ResearchAgent: Primary consumer.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class PerplexityClient:
    """
    Client for Perplexity AI API.
    Currently defaults to MOCK MODE as per Phase 11 requirements.
    Future: Will integrate Perplexity Sonar models.
    """
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # TODO: Initialize real Perplexity client here when live

    async def search(self, query: str) -> Dict[str, Any]:
        """
        Performs a search-augmented query.
        Returns: {
            "answer": str,
            "citations": List[str]
        }
        """
        if self.mock:
            # Simulate "thinking" and search latency
            await asyncio.sleep(1.2)
            return self._generate_mock_response(query)

        # Placeholder for live API call
        return {"answer": "Live Perplexity API not implemented.", "citations": []}

    def _generate_mock_response(self, query: str) -> Dict[str, Any]:
        """
        Returns a mock answer with citations based on the query.
        """
        query_lower = query.lower()
        
        if "nvda" in query_lower or "nvidia" in query_lower:
            return {
                "answer": ("NVIDIA (NVDA) is currently trading near all-time highs, driven by "
                           "sustained demand for its H100 AI advice chips [1]. Analysts have "
                           "recently raised price targets, citing a 30% increase in data center "
                           "revenue year-over-year [2]. However, some concern remains regarding "
                           "supply chain constraints and potential regulatory headwinds in "
                           "China [3]."),
                "citations": [
                    "https://www.bloomberg.com/news/articles/2026-01-20/nvidia-earnings-preview",
                    "https://www.cnbc.com/2026/01/21/analyst-upgrades-nvda-price-target.html",
                    "https://www.reuters.com/technology/nvidia-china-export-restrictions-2026-01-15/"
                ]
            }
        
        elif "cpi" in query_lower or "inflation" in query_lower:
            return {
                "answer": ("The latest CPI print came in at 2.8% YoY, slightly above the consensus "
                           "estimate of 2.6% [1]. Core inflation remains sticky in the services "
                           "sector, which may prompt the Fed to hold rates steady for longer [2]. "
                           "Market reaction has been mixed, with ongoing rotation into value "
                           "stocks [3]."),
                "citations": [
                    "https://www.bls.gov/cpi/latest-release.htm",
                    "https://www.wsj.com/economy/central-banking/fed-rate-decision-outlook-2026",
                    "https://finance.yahoo.com/news/market-reaction-cpi-print-140000.html"
                ]
            }
            
        else:
            return {
                "answer": (f"Researching '{query}'... Market data suggests this sector is "
                           "currently volatile due to macroeconomic factors [1]. Institutional "
                           "flows have been neutral over the last trading week [2]. Caution is "
                           "advised until a clear trend emerges [3]."),
                "citations": [
                    "https://www.investopedia.com/terms/m/market_sentiment.asp",
                    "https://www.bloomberg.com/markets",
                    "https://www.vanguard.com/market-outlook"
                ]
            }

class PerplexityClientSingleton:
    """Singleton wrapper for PerplexityClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> PerplexityClient:
        """Returns the singleton instance of PerplexityClient."""
        if cls._instance is None:
            cls._instance = PerplexityClient(mock=mock)
        return cls._instance

def get_perplexity_client(mock: bool = True) -> PerplexityClient:
    """Legacy helper to get the perplexity client instance."""
    return PerplexityClientSingleton.get_instance(mock=mock)
