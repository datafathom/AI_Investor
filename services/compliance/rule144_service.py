"""
==============================================================================
FILE: services/compliance/rule144_service.py
ROLE: SEC Rule 144 Compliance Engine
PURPOSE: Calculate "Dribble Out" Volume Limits for Affiliates.
         - Limit 1: 1% of Shares Outstanding
         - Limit 2: Average Weekly Trading Volume (4 weeks)
         - Max Sale = Greater of (Limit 1, Limit 2) every 3 months.

INTEGRATION:
    - MarketDataService: Volume data.
    - CompanyDataService: Outstanding shares.
    - ComplianceService: Affiliate status.

AUTHOR: AI Investor Team
CREATED: 2026-01-30
==============================================================================
"""

import logging
from decimal import Decimal
from typing import Dict, List, Optional
from datetime import date

logger = logging.getLogger(__name__)

class Rule144Service:
    """
    Calculates sell limits for Control Persons / Affiliates.
    """

    def calculate_max_sale_quantity(
        self,
        ticker: str,
        shares_outstanding: int,
        weekly_volumes: List[int]
    ) -> Dict[str, Any]:
        """
        Calculate the volume limit for Rule 144 sales.
        
        Args:
            weekly_volumes: List of volume sums for the last 4 calendar weeks.
        """
        if not weekly_volumes:
            logger.warning(f"No volume data for {ticker}")
            return {"max_sale_qty": 0, "reason": "No Volume Data"}

        # Limit 1: 1% of Outstanding
        limit_1_pct = int(shares_outstanding * 0.01)

        # Limit 2: Average Weekly Volume (Trailing 4 Weeks)
        # Note: Rule 144(e) specifies the average weekly reported volume for the 
        # four calendar weeks preceding the filing of verify.
        avg_weekly_vol = int(sum(weekly_volumes) / len(weekly_volumes))

        # Max Sale is the GREATER of the two
        max_limit = max(limit_1_pct, avg_weekly_vol)

        return {
            "ticker": ticker,
            "limit_1_pct_outstanding": limit_1_pct,
            "limit_avg_weekly_volume": avg_weekly_vol,
            "max_sale_quantity_3mo": max_limit,
            "status": "CALCULATED"
        }

    def check_affiliate_status(self, client_id: str, ticker: str) -> bool:
        # Mock logic
        # In prod: graph query (:CLIENT)-[:IS_AFFILIATE_OF]->(:COMPANY)
        return True
