"""
==============================================================================
FILE: services/ai/gemini_client.py
ROLE: AI Model Client
PURPOSE: Interfaces with Google Gemini API (or Mock) for generating 
         morning briefings and market summaries.
         
INTEGRATION POINTS:
    - APIGovernor: Manages Gemini rate limits (if live).
    - BriefingGenerator: Primary consumer for daily reports.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import logging
import asyncio
import datetime
import random
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Client for Google Gemini API.
    Currently defaults to MOCK MODE as per Phase 10 requirements.
    """
    def __init__(self, api_key: Optional[str] = None, mock: bool = True):
        self.mock = mock
        self.api_key = api_key
        # If live, we would initialize the Google AI SDK client here

    async def generate_briefing(self, date: datetime.date) -> Dict[str, Any]:
        """
        Generates a structured morning briefing.
        """
        if self.mock:
            # Simulate generation time
            await asyncio.sleep(2.0)
            return self._generate_mock_briefing(date)

        return {}

    def _generate_mock_briefing(self, date: datetime.date) -> Dict[str, Any]:
        """
        Returns a mock briefing structure.
        """
        date_str = date.strftime("%B %d, %Y")
        return {
            "date": date_str,
            "sentiment": random.choice(["BULLISH", "NEUTRAL", "BEARISH"]),
            "market_outlook": (
                f"Global markets are {random.choice(['trending higher', 'mixed', 'pulling back'])} "
                "this morning as investors digest the latest "
                f"{random.choice(['inflation data', 'jobs report', 'central bank meeting', 'earnings results'])}. "
                "Tech continues to lead, while defensive sectors lag."
            ),
            "key_events": [
                {"time": "8:30 AM", "event": "CPI Data Release", "impact": "HIGH"},
                {"time": "10:00 AM", "event": "Consumer Confidence", "impact": "MEDIUM"},
                {"time": "2:00 PM", "event": "Fed Minutes", "impact": "HIGH"}
            ],
            "portfolio_alerts": [
                {"ticker": "NVDA", "message": "Approaching all-time highs. RSI overbought (75).",
                 "type": "warning"},
                {"ticker": "AAPL", "message": "Golden cross detected on 4H chart.", "type": "info"},
                {"ticker": "TSLA", "message": "High social volume detected on r/wallstreetbets.",
                 "type": "alert"}
            ],
            "quote_of_the_day": ("The stock market is designed to transfer money from the Active to the "
                                "Patient. - Warren Buffett")
        }

class GeminiClientSingleton:
    """Singleton wrapper for GeminiClient."""
    _instance = None

    @classmethod
    def get_instance(cls, mock: bool = True) -> GeminiClient:
        """Returns the singleton instance of GeminiClient."""
        if cls._instance is None:
            cls._instance = GeminiClient(mock=mock)
        return cls._instance

def get_gemini_client(mock: bool = True) -> GeminiClient:
    """Legacy helper to get the gemini client instance."""
    return GeminiClientSingleton.get_instance(mock=mock)
