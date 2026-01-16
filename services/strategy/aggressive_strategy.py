"""
==============================================================================
FILE: services/strategy/aggressive_strategy.py
ROLE: Aggressive Portfolio Alpha
PURPOSE:
    Manage the "Risk-On" component of the portfolio.
    - Select High Growth Assets (High Beta, Momentum, Social Sentiment)
    - Dynamically allocate capital based on Market Regime (Fear/Greed).
    
    Logic:
    - RISK ON:
      - When Fear Index is LOW (Greed is High), sentiment is bullish. 
      - However, Extreme Greed (>80) is a sell signal (Reversal risk).
      - Extreme Fear (<20) is a buy signal (Deep Value), but maybe dangerous for "Momentum".
      
      Sweet Spot Strategy (Momentum/Trend Following):
      - We want to ride the wave.
      - Best time for Aggressive: Fear Index 40-60 (Neutral/Climbing) OR < 40 (Bull market).
      - Stop Loss: If Fear Index > 80 (Overheated), trim exposure?
      
      Let's stick to the "Goldilocks" Logic from Roadmap:
      - "Allocation increases when 'Goldilocks' regime".
      
      Implementation:
      - Fear < 40 (Neutral/Fear): + Allocation (Buy the Dip / Accumulate)
      - Fear 40-60: Max Allocation (Trend is friend)
      - Fear > 60: Reduce Allocation (Risk Off)
      
ROADMAP: Phase 17 - Aggressive Alpha
==============================================================================
"""

import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AggressiveStrategy:
    def __init__(self):
        pass

    def select_aggressive_assets(self, assets_data: Dict[str, pd.DataFrame]) -> List[str]:
        """
        Select assets suitable for Aggressive Alpha.
        Criteria:
        - Beta > 1.2 (High sensitivity to market) [Proxy: High Volatility relative to baseline]
        - Momentum > 0 (Must be in uptrend)
        """
        aggressive_assets = []
        for symbol, df in assets_data.items():
            if df.empty or len(df) < 20:
                continue
                
            # Quick Momentum Check (Last 20 days)
            momentum = df['close'].pct_change(periods=20).iloc[-1]
            
            # Quick Volatility/Beta Proxy
            vol = df['close'].pct_change().std() * (252 ** 0.5)
            
            # Criteria: High Volatility (Aggressive) AND Positive Momentum
            if vol > 0.30 and momentum > 0:
                aggressive_assets.append(symbol)
                
        return aggressive_assets

    def calculate_aggressive_allocation(self, fear_greed_index: float) -> float:
        """
        Determine % allocation to Aggressive Alpha.
        
        Logic:
        - Fear 0-40 (Fear/Extreme Fear): 40% (Accumulate)
        - Fear 40-60 (Neutral): 60% (Max Aggression, Trend is healthy)
        - Fear 60-80 (Greed): 30% (Take profits)
        - Fear > 80 (Extreme Greed): 0% (Exit/Hedge)
        """
        if fear_greed_index > 80:
            return 0.0
        elif fear_greed_index > 60:
            return 0.3
        elif fear_greed_index > 40:
            return 0.6
        else:
            # Low fear usually means bottoms or bear market. 
            # If we assume "Buy Low", we accumulate.
            return 0.4

# Singleton
_instance = None

def get_aggressive_strategy() -> AggressiveStrategy:
    global _instance
    if _instance is None:
        _instance = AggressiveStrategy()
    return _instance
