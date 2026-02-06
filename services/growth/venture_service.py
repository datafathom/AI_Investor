"""
Venture Service
Phase 8 Implementation: The Global HQ

Handles Venture Capital deal modeling, Cap-Table math, and Exit Waterfalls.
"""

import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ShareClass(BaseModel):
    name: str # e.g. "Series A"
    shares: int
    price_per_share: float
    liquidation_preference: float = 1.0 # 1x, 2x, etc.
    is_participating: bool = False
    is_preferred: bool = True

class VentureService:
    """
    Core engine for Cap-Table Waterfall and Dilution modeling.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VentureService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("VentureService initialized")

    def calculate_waterfall(self, 
                           exit_value: float, 
                           cap_table: List[ShareClass], 
                           common_shares: int) -> Dict[str, Any]:
        """
        Calculates the exit proceeds for each share class.
        """
        remaining_proceeds = exit_value
        results = {}
        total_preferred_payout = 0

        # 1. Preferred Returns (Liquidation Preference)
        # Sorted by seniority (assumed list order for now: senior first)
        for sc in cap_table:
            if not sc.is_preferred:
                continue
            
            preference_payout = min(remaining_proceeds, 
                                   sc.shares * sc.price_per_share * sc.liquidation_preference)
            results[sc.name] = {
                "preference_payout": preference_payout,
                "common_payout": 0.0,
                "total_payout": preference_payout
            }
            remaining_proceeds -= preference_payout
            total_preferred_payout += preference_payout

        # 2. Common Distribution
        # Participating Preferred + Common
        participating_shares = sum([sc.shares for sc in cap_table if sc.is_participating])
        total_common_pool_shares = participating_shares + common_shares
        
        if total_common_pool_shares > 0 and remaining_proceeds > 0:
            price_per_common = remaining_proceeds / total_common_pool_shares
            
            # Common Shareholders
            results["Common"] = {
                "preference_payout": 0.0,
                "common_payout": common_shares * price_per_common,
                "total_payout": common_shares * price_per_common
            }
            
            # Participating Preferred Shareholders
            for sc in cap_table:
                if sc.is_participating:
                    additional = sc.shares * price_per_common
                    results[sc.name]["common_payout"] = additional
                    results[sc.name]["total_payout"] += additional

        return {
            "exit_value": exit_value,
            "distributable_proceeds": exit_value,
            "payouts": results,
            "price_per_common": remaining_proceeds / total_common_pool_shares if total_common_pool_shares > 0 else 0
        }

    def simulate_dilution(self, 
                          current_shares: int, 
                          new_investment: float, 
                          pre_money_valuation: float) -> Dict[str, Any]:
        """
        Simulates a new funding round.
        """
        post_money = pre_money_valuation + new_investment
        price_per_share = pre_money_valuation / current_shares
        new_shares = int(new_investment / price_per_share)
        total_shares = current_shares + new_shares
        
        dilution = new_shares / total_shares
        
        return {
            "pre_money": pre_money_valuation,
            "post_money": post_money,
            "price_per_share": price_per_share,
            "new_shares": new_shares,
            "total_shares": total_shares,
            "dilution_percentage": dilution * 100
        }

def get_venture_service() -> VentureService:
    return VentureService()
