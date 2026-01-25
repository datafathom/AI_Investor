"""
==============================================================================
FILE: services/trading/ipo_tracker.py
ROLE: Analysis & Monitoring Engine
PURPOSE: Monitors upcoming IPOs, calculates success probabilities, and 
         generates alerts for high-conviction listings.
         
INTEGRATION POINTS:
    - FinnhubClient: Source of IPO data.
    - NotificationService: Sends alerts (future).
    - Database: Persists tracked IPOs (future).

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
from typing import List, Optional
from pydantic import BaseModel
from services.data.finnhub_service import get_finnhub_client, FinnhubIPO

logger = logging.getLogger(__name__)

class IPOAnalysis(BaseModel):
    """Pydantic model for IPO analysis results."""
    symbol: str
    company: str
    date: str
    success_probability: float  # 0-100
    risk_score: float  # 0-100
    sentiment_signal: str  # BULLISH, NEUTRAL, BEARISH
    estimated_valuation: Optional[str]

class IPOTracker:
    """
    Service to track and analyze upcoming IPOs.
    """

    def __init__(self, finnhub_client=None):
        self.finnhub = finnhub_client or get_finnhub_client()

    async def get_upcoming_analysis(self, days: int = 30) -> List[IPOAnalysis]:
        """
        Retrieves and analyzes upcoming IPOs.
        """
        _ = days  # Unused in current implementation
        ipos = await self.finnhub.get_ipo_calendar()
        if not ipos:
            return []

        results = []
        for ipo in ipos:
            analysis = self._analyze_ipo(ipo)
            results.append(analysis)

        return results

    def _analyze_ipo(self, ipo: FinnhubIPO) -> IPOAnalysis:
        """
        Heuristic-based IPO analysis.
        """
        # 1. Base Probability
        prob = 50.0
        risk = 50.0
        signal = "NEUTRAL"

        # 2. Status check
        if ipo.status.lower() == "expected":
            prob += 10
        elif ipo.status.lower() == "priced":
            prob += 20
            risk -= 10

        # 3. Sector analysis (Placeholder - in real app would use company profile)
        # Tech/AI often gets higher BULLISH signal in current market
        tech_keywords = ["tech", "software", "ai", "intelligence", "cloud"]
        if any(kw in ipo.company.lower() for kw in tech_keywords):
            prob += 15
            signal = "BULLISH"

        # 4. Valuation / Price Range check
        if ipo.price_range and "-" in ipo.price_range:
            try:
                # If high-end is significantly above low-end, might imply demand
                low, high = [float(p.strip()) for p in ipo.price_range.split("-")]
                if (high / low) > 1.2:
                    risk += 10
            except (ValueError, ZeroDivisionError):
                pass

        # Cap results
        prob = max(5.0, min(95.0, prob))
        risk = max(5.0, min(95.0, risk))

        return IPOAnalysis(
            symbol=ipo.symbol,
            company=ipo.company,
            date=ipo.date,
            success_probability=prob,
            risk_score=risk,
            sentiment_signal=signal,
            estimated_valuation=ipo.price_range
        )

class IPOTrackerSingleton:
    """Singleton wrapper for IPOTracker."""
    _instance = None

    @classmethod
    def get_instance(cls) -> IPOTracker:
        """Returns the singleton instance of IPOTracker."""
        if cls._instance is None:
            cls._instance = IPOTracker()
        return cls._instance

def get_ipo_tracker() -> IPOTracker:
    """Legacy helper to get the IPO tracker instance."""
    return IPOTrackerSingleton.get_instance()
