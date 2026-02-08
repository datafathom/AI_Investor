"""
==============================================================================
FILE: services/market_data/forced_seller_svc.py
ROLE: Market Intelligence - Fragility Analysis
PURPOSE: Tracks passive ownership concentration and structural fragility risks.
         Provides early warnings for liquidity traps and forced seller pressure.
==============================================================================
"""

import logging
import random
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

# Mock data for demonstration
MOCK_TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD", "INTC", "SPY"]
SECTORS = ["Technology", "Consumer", "Healthcare", "Finance", "Energy", "Materials"]

class ForcedSellerService:
    """
    Service for analyzing forced seller risk and liquidity fragility.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ForcedSellerService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("ForcedSellerService initialized")

    def calculate_fragility_score(self, ticker: str) -> Dict[str, Any]:
        """
        Calculate fragility score (0-100) for a given ticker.
        Factors: Passive %, Float Turnover, Bid-Ask Spread Volatility
        """
        # Deterministic-ish random based on ticker
        random.seed(sum(ord(c) for c in ticker))
        
        passive_pct = random.uniform(15.0, 75.0)
        float_turnover = random.uniform(0.5, 3.0)
        spread_vol = random.uniform(0.01, 0.15)

        # Weighted score calculation: Passive % is a huge risk multiplier in structural fragility
        score = (passive_pct * 0.6) + (20 / float_turnover) + (spread_vol * 150)
        score = min(100, max(0, score))

        risk_level = "LOW" if score < 40 else ("MEDIUM" if score < 70 else "HIGH")

        return {
            "ticker": ticker,
            "passive_pct": round(passive_pct, 2),
            "float_turnover": round(float_turnover, 2),
            "spread_volatility": round(spread_vol, 4),
            "fragility_score": round(score, 1),
            "risk_level": risk_level,
            "last_updated": datetime.now().isoformat()
        }

    def get_top_fragile_tickers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns top tickers by fragility score.
        """
        results = [self.calculate_fragility_score(t) for t in MOCK_TICKERS]
        results.sort(key=lambda x: x["fragility_score"], reverse=True)
        return results[:limit]

    def get_passive_heatmap(self) -> List[Dict[str, Any]]:
        """
        Aggregates passive ownership data by sector for heatmap visualization.
        """
        heatmap = []
        for sector in SECTORS:
            # Deterministic for sector
            random.seed(sum(ord(c) for c in sector))
            avg_passive = random.uniform(25, 55)
            high_risk = random.randint(0, 4)
            
            heatmap.append({
                "sector": sector,
                "avg_passive_pct": round(avg_passive, 1),
                "total_fragility": round(random.uniform(35, 75), 1),
                "ticker_count": random.randint(12, 45),
                "high_risk_count": high_risk
            })
        return heatmap

    def get_liquidity_traps(self) -> List[Dict[str, Any]]:
        """
        Detects active liquidity traps (bid-ask expansion > 2.5x).
        """
        # Occasionally return a trap for AAPL or NVDA
        traps = []
        if random.random() > 0.7:
            traps.append({
                "ticker": random.choice(["AAPL", "NVDA", "TSLA"]),
                "spread_expansion": round(random.uniform(2.5, 4.8), 2),
                "timestamp": datetime.now().isoformat(),
                "severity": random.choice(["MODERATE", "SEVERE", "CRITICAL"])
            })
        return traps


def get_forced_seller_service() -> ForcedSellerService:
    return ForcedSellerService()
