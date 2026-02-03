"""
==============================================================================
FILE: services/analysis/short_interest_service.py
ROLE: Analysis Engine
PURPOSE: Processes short interest data from Quandl to identify squeeze
         opportunities and risk levels.
         
INTEGRATION POINTS:
    - QuandlClient: Source of short interest data
    - AlphaVantageClient: Source of volume data
    - RiskEngine: Consumes squeeze probability scores

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from services.data.quandl_service import get_quandl_client, ShortInterestModel
from services.data.alpha_vantage import get_alpha_vantage_client

logger = logging.getLogger(__name__)

class SqueezeAnalysis(BaseModel):
    """Analysis result for short interest."""
    symbol: str
    short_ratio: float
    days_to_cover: float
    squeeze_probability: float  # 0-100
    risk_level: str  # Low, Medium, High, Extreme
    avg_daily_volume: float

class ShortInterestService:
    """
    Service to perform short interest and squeeze analysis.
    """

    def __init__(self, quandl_client=None, av_client=None):
        self.quandl = quandl_client or get_quandl_client()
        self.av = av_client or get_alpha_vantage_client()

    def analyze_symbol(self, symbol: str) -> Optional[SqueezeAnalysis]:
        """
        Performs full short interest analysis for a symbol.
        """
        # 1. Get Short Interest Data
        si_data = self.quandl.get_short_interest(symbol)
        if not si_data:
            logger.warning(f"No short interest data for {symbol}")
            return None

        latest_si = si_data[0]

        # 2. Get Average Daily Volume (10-day avg)
        # Note: In a real scenario, we'd fetch actual volume. For now, we'll try to get it from AV or fallback.
        avg_volume = 0.0
        try:
            daily_bars = self.av.get_daily(symbol, outputsize="compact")
            if daily_bars:
                # Average of last 10 days
                recent_bars = daily_bars[:10]
                avg_volume = sum(bar.volume for bar in recent_bars) / len(recent_bars)
        except Exception as e:
            logger.error(f"Error fetching volume for {symbol}: {e}")
            # Fallback to SI total volume if AV fails
            avg_volume = latest_si.total_volume

        # 3. Calculate Metrics
        short_ratio = latest_si.short_ratio
        days_to_cover = (latest_si.short_volume / avg_volume) if avg_volume > 0 else 0
        
        # 4. Calculate Squeeze Probability (Heuristic)
        # Factors: High Short Ratio (>0.2), High Days to Cover (>5), Recent Price Action (placeholder)
        prob = 0.0
        if short_ratio > 0.3: prob += 40
        elif short_ratio > 0.2: prob += 20
        
        if days_to_cover > 10: prob += 40
        elif days_to_cover > 5: prob += 20
        
        # Cap at 95 unless we have price triggers
        prob = min(prob, 95.0)

        # 5. Determine Risk Level
        if prob > 80: risk_level = "EXTREME"
        elif prob > 60: risk_level = "HIGH"
        elif prob > 30: risk_level = "MEDIUM"
        else: risk_level = "LOW"

        return SqueezeAnalysis(
            symbol=symbol,
            short_ratio=short_ratio,
            days_to_cover=days_to_cover,
            squeeze_probability=prob,
            risk_level=risk_level,
            avg_daily_volume=avg_volume
        )

_instance = None

def get_short_interest_service() -> ShortInterestService:
    global _instance
    if _instance is None:
        _instance = ShortInterestService()
    return _instance
