
import pytest
import pandas as pd
import numpy as np
from services.strategy.aggressive_strategy import AggressiveStrategy

class TestAggressiveStrategy:
    
    def test_aggressive_allocation_logic(self):
        strategy = AggressiveStrategy()
        
        # > 80 (Extreme Greed) -> 0% (Exit)
        assert strategy.calculate_aggressive_allocation(85) == 0.0
        
        # 40-60 (Neutral/Trend) -> 60% (Max)
        assert strategy.calculate_aggressive_allocation(50) == 0.6
        
        # < 40 (Fear) -> 40% (Accumulate)
        assert strategy.calculate_aggressive_allocation(30) == 0.4

    def test_select_aggressive_assets(self):
        strategy = AggressiveStrategy()
        
        # Asset A: High Vol + Positive Momentum (Crypto-like)
        # Rising trend with noise
        df_a = pd.DataFrame({'close': np.linspace(100, 150, 100) + np.random.normal(0, 5, 100)}) 
        
        # Asset B: Low Vol (Bond-like)
        df_b = pd.DataFrame({'close': np.linspace(100, 101, 100) + np.random.normal(0, 0.1, 100)})
        
        # Asset C: High Vol but Negative Momentum (Crash)
        df_c = pd.DataFrame({'close': np.linspace(100, 50, 100) + np.random.normal(0, 5, 100)})
        
        assets = {'CRYPTO': df_a, 'BOND': df_b, 'CRASH': df_c}
        
        selection = strategy.select_aggressive_assets(assets)
        
        assert 'CRYPTO' in selection
        assert 'BOND' not in selection
        assert 'CRASH' not in selection
