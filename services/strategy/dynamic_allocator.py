"""
==============================================================================
FILE: services/strategy/dynamic_allocator.py
ROLE: Chief Investment Officer (CIO) / Portfolio Orchestrator
PURPOSE:
    Combine signals from Defensive (Shield) and Aggressive (Alpha) strategies
    to determine final asset allocation.
    
    Logic:
    - Get Shield % from DefensiveStrategy
    - Get Alpha % from AggressiveStrategy
    - Remainder = Cash (or Gold/Treasuries if implemented as specific assets)
    - If Total > 100%, normalize weights (Leverage not fully enabled yet).
    
ROADMAP: Phase 18 - Dynamic Allocator
==============================================================================
"""

import logging
from typing import Dict, Any, List
import pandas as pd

from services.strategy.defensive_strategy import get_defensive_strategy
from services.strategy.aggressive_strategy import get_aggressive_strategy

logger = logging.getLogger(__name__)

class DynamicAllocator:
    def __init__(self):
        self.defensive = get_defensive_strategy()
        self.aggressive = get_aggressive_strategy()

    def get_regime(self, fear_index: float) -> str:
        """
        Classify market regime based on Fear & Greed Index.
        """
        if fear_index < 25:
            return "EXTREME_FEAR"
        elif fear_index < 45:
            return "FEAR"
        elif fear_index < 55:
            return "NEUTRAL"
        elif fear_index < 75:
            return "GREED"
        else:
            return "EXTREME_GREED"

    def allocate_capital(self, fear_index: float) -> Dict[str, float]:
        """
        Determine high-level allocation buckets.
        Returns: {'SHIELD': 0.x, 'ALPHA': 0.y, 'CASH': 0.z}
        """
        shield_pct = self.defensive.calculate_shield_allocation(fear_index)
        alpha_pct = self.aggressive.calculate_aggressive_allocation(fear_index)
        
        total_deployed = shield_pct + alpha_pct
        
        # Normalization if > 100% (No leverage yet)
        if total_deployed > 1.0:
            scale = 1.0 / total_deployed
            shield_pct *= scale
            alpha_pct *= scale
            cash_pct = 0.0
        else:
            cash_pct = 1.0 - total_deployed
            
        return {
            "SHIELD": round(shield_pct, 4),
            "ALPHA": round(alpha_pct, 4),
            "CASH": round(cash_pct, 4)
        }

    def construct_target_portfolio(self, 
                                 assets_map: Dict[str, pd.DataFrame], 
                                 fear_index: float) -> Dict[str, float]:
        """
        Generate specific asset weights for the entire portfolio.
        
        1. Determine Buckets (Shield vs Alpha vs Cash)
        2. Select Assets for each bucket
        3. Distribute bucket weight among selected assets (Equal Weight for now)
        """
        allocations = self.allocate_capital(fear_index)
        portfolio_weights = {}
        
        # 1. SHIELD ASSETS
        if allocations['SHIELD'] > 0:
            safe_assets = self.defensive.filter_safe_assets(assets_map)
            if safe_assets:
                weight_per_asset = allocations['SHIELD'] / len(safe_assets)
                for asset in safe_assets:
                    portfolio_weights[asset] = weight_per_asset
            else:
                # Fallback to Cash if no safe assets found
                allocations['CASH'] += allocations['SHIELD']
                allocations['SHIELD'] = 0

        # 2. ALPHA ASSETS
        if allocations['ALPHA'] > 0:
            alpha_assets = self.aggressive.select_aggressive_assets(assets_map)
            if alpha_assets:
                weight_per_asset = allocations['ALPHA'] / len(alpha_assets)
                for asset in alpha_assets:
                    portfolio_weights[asset] = weight_per_asset
            else:
                # Fallback to Cash
                allocations['CASH'] += allocations['ALPHA']
                allocations['ALPHA'] = 0
                
        # 3. CASH (Represented as 'USD' or 'CASH')
        if allocations['CASH'] > 0:
            portfolio_weights['CASH'] = allocations['CASH']
            
        return portfolio_weights

# Singleton
_instance = None

def get_dynamic_allocator() -> DynamicAllocator:
    global _instance
    if _instance is None:
        _instance = DynamicAllocator()
    return _instance
