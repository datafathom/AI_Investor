"""
==============================================================================
FILE: services/strategy/defensive_strategy.py
ROLE: Defensive Portfolio Shield
PURPOSE:
    Manage the "Safety" component of the portfolio.
    - Select Safe Assets (Low Beta, Low Volatility)
    - Dynamically allocate capital to Shield based on Market Regime (Fear/Greed).
    
    Logic:
    - CONTRARIAN APPROACH (Buy Fear, Sell Greed?):
      Wait, Defensive Shield usually means "Safety". 
      When Market is Risk-Off (Fear), we might want MORE Shield if we think it's a crash.
      BUT, "Buy the Dip" implies entering Risk Assets when Fear is high.
      
      Let's implement the 'Rotational' Logic:
      - Extreme Fear (<20): MARKET CRASH? -> If VIX is spiking, hold Cash/Shield. 
        OR, if we are smart, this is buying time.
        
      Let's go with the SAFE STANDARD logic for a "Shield":
      - The Shield is the ANCHOR. 
      - High market risk (Bear Market) -> Increase Shield.
      - Low market risk (Bull Market) -> Decrease Shield.
      
      Proxy for market risk:
      - If Fear/Greed < 20 (Extreme Fear): Often means market is oversold. Opportunity? -> SHIELD OFF (0%).
      - If Fear/Greed > 80 (Extreme Greed): Market is frothy. Correction likely? -> SHIELD ON (Alloc up to 60%).
      - Normal (40-60): Standard Shield (20%).
      
ROADMAP: Phase 16 - Defensive Shield
==============================================================================
"""

import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DefensiveStrategy:
    def __init__(self):
        # Thresholds for Fear & Greed Index
        self.EXTREME_FEAR = 20
        self.FEAR = 40
        self.GREED = 60
        self.EXTREME_GREED = 80

    def filter_safe_assets(self, assets_data: Dict[str, pd.DataFrame]) -> List[str]:
        """
        Select assets suitable for the Defensive Shield.
        Criteria:
        - Beta < 0.8 (Lower correlation to market) [Simplification: Volatility check for now]
        - Rolling Volatility < Market Volatility
        """
        safe_assets = []
        for symbol, df in assets_data.items():
            if df.empty:
                continue
                
            # Quick Volatility Check (Annualized)
            # Assuming daily data
            returns = df['close'].pct_change().dropna()
            vol = returns.std() * (252 ** 0.5)
            
            # Arbitrary threshold for "Low Vol" (e.g. < 20%)
            # Ideally this compares against SPY vol.
            if vol < 0.25: 
                safe_assets.append(symbol)
                
        return safe_assets

    def calculate_shield_allocation(self, fear_greed_index: float) -> float:
        """
        Determine the % of portfolio to allocate to the Defensive Shield
        based on the Fear & Greed Index (0-100).
        
        Logic (Contrarian / Protection):
        - Index < 20 (Extreme Fear): BUY SIGNAL. Reduce Shield -> 0% (Deploy capital)
        - Index > 80 (Extreme Greed): SELL SIGNAL. Increase Shield -> 50% (Lock gains)
        - Index 50 (Neutral): Base Shield -> 20%
        """
        
        # Linear Interpolation or Tiered logic
        
        if fear_greed_index <= 20:
            # Extreme Fear: Be Greedy. Min Shield.
            return 0.0
        
        elif fear_greed_index >= 80:
            # Extreme Greed: Be Fearful. Max Shield.
            return 0.60 # 60% Safety
            
        else:
            # Linear ramp mapping 20->80 to 0.0->0.6
            # Slope = (0.6 - 0.0) / (80 - 20) = 0.6 / 60 = 0.01
            # Alloc = 0.0 + 0.01 * (index - 20)
            
            return 0.01 * (fear_greed_index - 20)

# Singleton
_instance = None

def get_defensive_strategy() -> DefensiveStrategy:
    global _instance
    if _instance is None:
        _instance = DefensiveStrategy()
    return _instance
