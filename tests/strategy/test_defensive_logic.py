
import pytest
import pandas as pd
import numpy as np
from services.strategy.defensive_strategy import DefensiveStrategy

class TestDefensiveStrategy:
    
    def test_shield_allocation_logic(self):
        strategy = DefensiveStrategy()
        
        # Extreme Fear -> 0% Shield (Buy)
        assert strategy.calculate_shield_allocation(10) == 0.0
        assert strategy.calculate_shield_allocation(20) == 0.0
        
        # Extreme Greed -> 60% Shield (Protect)
        assert strategy.calculate_shield_allocation(80) == 0.6
        assert strategy.calculate_shield_allocation(90) == 0.6
        
        # Neutral (50) -> 30% Shield
        # 0.01 * (50 - 20) = 0.3
        assert abs(strategy.calculate_shield_allocation(50) - 0.3) < 0.001

    def test_filter_safe_assets(self):
        strategy = DefensiveStrategy()
        
        # Asset A: Low Vol (Flat line with tiny noise)
        df_a = pd.DataFrame({'close': np.linspace(100, 101, 252) + np.random.normal(0, 0.1, 252)})
        
        # Asset B: High Vol (Wild swings)
        df_b = pd.DataFrame({'close': np.linspace(100, 100, 252) + np.random.normal(0, 5, 252)})
        
        assets = {'LOW_VOL': df_a, 'HIGH_VOL': df_b}
        
        safe = strategy.filter_safe_assets(assets)
        
        assert 'LOW_VOL' in safe
        assert 'HIGH_VOL' not in safe
