"""
==============================================================================
FILE: services/market_data/whale_flow_service.py
ROLE: Market Intelligence - Institutional Flow Tracking
PURPOSE: Analyzes 13F filings, whale selling pressure, and sector overcrowding.
==============================================================================
"""

import logging
import random
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

MOCK_HOLDERS = [
    "BlackRock", "Vanguard", "State Street", "Fidelity", "Capital Group",
    "T. Rowe Price", "JP Morgan", "Goldman Sachs", "Morgan Stanley", "Citadel"
]

MOCK_TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD", "INTC", "SPY"]
SECTORS = ["Technology", "Consumer", "Healthcare", "Finance", "Energy", "Materials"]


class WhaleFlowService:
    """
    Service for tracking institutional whale activity from 13F filings.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WhaleFlowService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("WhaleFlowService initialized")

    def get_whale_flow_summary(self) -> Dict[str, Any]:
        """Get summary of recent whale activity."""
        # Seed for some stability in results during a session
        current_quarter = (datetime.now().month - 1) // 3 + 1
        random.seed(current_quarter)
        
        return {
            "total_filings_this_quarter": random.randint(120, 450),
            "net_buying_billions": round(random.uniform(-12, 25), 2),
            "most_bought_ticker": random.choice(MOCK_TICKERS),
            "most_sold_ticker": random.choice(MOCK_TICKERS),
            "average_position_change_pct": round(random.uniform(-8, 12), 2),
            "last_updated": datetime.now().isoformat()
        }

    def get_ticker_whale_activity(self, ticker: str) -> Dict[str, Any]:
        """Get whale activity for a specific ticker."""
        random.seed(sum(ord(c) for c in ticker))
        holders = []
        for holder in random.sample(MOCK_HOLDERS, k=random.randint(4, 9)):
            holders.append({
                "name": holder,
                "change_shares": random.randint(-2500000, 5000000),
                "change_pct": round(random.uniform(-15.0, 45.0), 2),
                "current_shares": random.randint(10000000, 150000000),
                "filing_date": (datetime.now() - timedelta(days=random.randint(1, 45))).strftime("%Y-%m-%d")
            })
        
        return {
            "ticker": ticker.upper(),
            "holders": holders,
            "net_institutional_change": sum(h["change_shares"] for h in holders),
            "total_institutional_holders": len(holders),
            "last_updated": datetime.now().isoformat()
        }

    def get_recent_filings(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent 13F filings."""
        filings = []
        for i in range(limit):
            # Deterministic sequence for variety
            idx = (datetime.now().hour + i) % len(MOCK_HOLDERS)
            t_idx = (datetime.now().day + i) % len(MOCK_TICKERS)
            
            action = "BUY" if i % 3 == 0 else ("SELL" if i % 3 == 1 else "HOLD")
            change = random.randint(100000, 5000000) if action != "HOLD" else 0
            if action == "SELL": change = -change

            filings.append({
                "holder": MOCK_HOLDERS[idx],
                "filing_date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "ticker": MOCK_TICKERS[t_idx],
                "action": action,
                "shares_changed": change,
                "position_value_millions": round(random.uniform(50, 1200), 2)
            })
        return filings

    def get_sector_crowding(self) -> List[Dict[str, Any]]:
        """Analyze sector crowding from institutional positions."""
        crowding = []
        for i, sector in enumerate(SECTORS):
            random.seed(sum(ord(c) for c in sector))
            score = random.randint(45, 98)
            
            # Simulated history for timeline/charts
            history = []
            for d in range(12, -1, -1):
                history.append({
                    "date": (datetime.now() - timedelta(weeks=d)).strftime("%Y-%m-%d"),
                    "score": max(0, min(100, score + random.randint(-10, 10)))
                })

            crowding.append({
                "sector": sector,
                "crowding_score": score,
                "status": "OVERCROWDED" if score > 85 else ("HIGH" if score > 70 else "NORMAL"),
                "top_crowded_tickers": random.sample(MOCK_TICKERS, k=3),
                "avg_holder_overlap": round(random.uniform(0.4, 0.9), 2),
                "history": history
            })
        return sorted(crowding, key=lambda x: x["crowding_score"], reverse=True)

    def get_holder_details(self, holder_name: str) -> Dict[str, Any]:
        """Get detailed holdings for a specific institutional holder."""
        random.seed(sum(ord(c) for c in holder_name))
        holdings = []
        for ticker in random.sample(MOCK_TICKERS, k=random.randint(6, 10)):
            val = round(random.uniform(100, 5000), 2)
            holdings.append({
                "ticker": ticker,
                "shares": random.randint(5000000, 100000000),
                "value_millions": val,
                "pct_of_portfolio": round(random.uniform(1.5, 12.0), 2),
                "last_change_pct": round(random.uniform(-25.0, 50.0), 2)
            })
        
        return {
            "holder_name": holder_name,
            "aum_billions": round(random.uniform(500, 10000), 1),
            "total_positions": len(holdings) * 5,  # Simulated depth
            "top_holdings": sorted(holdings, key=lambda x: x["value_millions"], reverse=True)[:5],
            "portfolio_composition": holdings,
            "last_filing_date": (datetime.now() - timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")
        }


def get_whale_flow_service() -> WhaleFlowService:
    return WhaleFlowService()
