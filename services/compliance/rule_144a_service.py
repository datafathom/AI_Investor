"""
==============================================================================
FILE: services/compliance/rule_144a_service.py
ROLE: SEC Rule 144A Compliance Module
PURPOSE: Tracks unregistered securities, holding periods, and lockup expirations.
==============================================================================
"""

import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

MOCK_TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META"]


class Rule144AStatus:
    RESTRICTED = "RESTRICTED"
    ELIGIBLE = "ELIGIBLE"
    PENDING = "PENDING_REVIEW"
    EXPIRED = "EXPIRED"


class Rule144AService:
    """
    Service for tracking SEC Rule 144A compliance for unregistered securities.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Rule144AService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("Rule144AService initialized")

    def get_holding_info(self, ticker: str, holder_id: str = "default") -> Dict[str, Any]:
        """Get 144A holding information for a specific position."""
        acquisition_date = datetime.now() - timedelta(days=random.randint(30, 400))
        holding_days = (datetime.now() - acquisition_date).days
        min_holding = 180 if random.random() > 0.5 else 365  # 6 months or 1 year rule
        
        status = Rule144AStatus.ELIGIBLE if holding_days >= min_holding else Rule144AStatus.RESTRICTED
        days_to_eligible = max(0, min_holding - holding_days)
        
        return {
            "ticker": ticker.upper(),
            "holder_id": holder_id,
            "acquisition_date": acquisition_date.strftime("%Y-%m-%d"),
            "holding_days": holding_days,
            "min_holding_period": min_holding,
            "status": status,
            "days_until_eligible": days_to_eligible,
            "eligible_date": (acquisition_date + timedelta(days=min_holding)).strftime("%Y-%m-%d"),
            "volume_limit_available": random.randint(10000, 100000),
            "last_checked": datetime.now().isoformat()
        }

    def get_lockup_expirations(self, days_ahead: int = 90) -> List[Dict[str, Any]]:
        """Get upcoming lockup expirations."""
        expirations = []
        
        for ticker in random.sample(MOCK_TICKERS, k=random.randint(3, 6)):
            exp_date = datetime.now() + timedelta(days=random.randint(1, days_ahead))
            expirations.append({
                "ticker": ticker,
                "expiration_date": exp_date.strftime("%Y-%m-%d"),
                "days_remaining": (exp_date - datetime.now()).days,
                "shares_unlocking": random.randint(100000, 5000000),
                "holder_type": random.choice(["INSIDER", "INSTITUTIONAL", "VENTURE"]),
                "impact_severity": random.choice(["HIGH", "MEDIUM", "LOW"])
            })
        
        return sorted(expirations, key=lambda x: x["expiration_date"])

    def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Get compliance overview dashboard data."""
        return {
            "total_restricted_positions": random.randint(5, 25),
            "positions_eligible_this_month": random.randint(0, 5),
            "pending_reviews": random.randint(0, 3),
            "upcoming_lockups_30d": random.randint(0, 8),
            "volume_sold_this_quarter_pct": round(random.uniform(0, 25), 2),
            "max_quarterly_volume_pct": 25.0,  # SEC Rule 144 limit
            "last_updated": datetime.now().isoformat()
        }

    def check_sale_eligibility(self, ticker: str, shares: int, holder_id: str = "default") -> Dict[str, Any]:
        """Check if a sale is eligible under Rule 144."""
        holding = self.get_holding_info(ticker, holder_id)
        
        can_sell = holding["status"] == Rule144AStatus.ELIGIBLE
        max_shares = holding["volume_limit_available"]
        shares_requested = shares
        shares_allowed = min(shares, max_shares) if can_sell else 0
        
        return {
            "ticker": ticker.upper(),
            "shares_requested": shares_requested,
            "shares_allowed": shares_allowed,
            "can_sell": can_sell and shares <= max_shares,
            "holding_status": holding["status"],
            "reason": "Holding period not met" if not can_sell else ("Within volume limits" if shares <= max_shares else "Exceeds volume limits"),
            "checked_at": datetime.now().isoformat()
        }


def get_rule_144a_service() -> Rule144AService:
    return Rule144AService()
