
import pytest
import pandas as pd
import numpy as np
from services.strategy.dynamic_allocator import DynamicAllocator

class TestDynamicAllocator:
    
    def test_allocate_capital_normalization(self):
        allocator = DynamicAllocator()
        
        # Test Normalization (hypothetical scenario where both might want 60%)
        # Fear 50:
        # Shield (Defensive): 0.3
        # Alpha (Aggressive): 0.6
        # Total: 0.9 -> Cash 0.1
        allocs = allocator.allocate_capital(50)
        assert allocs['SHIELD'] == 0.3
        assert allocs['ALPHA'] == 0.6
        assert round(allocs['CASH'], 1) == 0.1
        
    def test_allocate_capital_extremes(self):
        allocator = DynamicAllocator()
        
        # Extreme Greed (90):
        # Shield: 0.6
        # Alpha: 0.0
        # Cash: 0.4
        allocs = allocator.allocate_capital(90)
        assert allocs['SHIELD'] == 0.6
        assert allocs['ALPHA'] == 0.0
        assert allocs['CASH'] == 0.4
        
        # Extreme Fear (10):
        # Shield: 0.0
        # Alpha: 0.4
        # Cash: 0.6
        allocs = allocator.allocate_capital(10)
        assert allocs['SHIELD'] == 0.0
        assert allocs['ALPHA'] == 0.4
        assert allocs['CASH'] == 0.6

    def test_construct_target_portfolio(self):
        allocator = DynamicAllocator()
        
        # Assets
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100)
        
        # Safe Asset (Low Vol)
        df_safe = pd.DataFrame({'close': np.linspace(100, 101, 100) + np.random.normal(0, 0.1, 100)}) 
        
        # Growth Asset (High Vol + Momentum)
        df_growth = pd.DataFrame({'close': np.linspace(100, 200, 100) + np.random.normal(0, 5, 100)})
        
        assets = {'SAFE': df_safe, 'GROWTH': df_growth}
        
        # Neutral Market (50) -> Shield 30%, Alpha 60%
        # Expectations:
        # SAFE weight ~= 0.3
        # GROWTH weight ~= 0.6
        # CASH ~= 0.1
        
        weights = allocator.construct_target_portfolio(assets, 50)
        
        assert 'SAFE' in weights
        assert 'GROWTH' in weights
        assert abs(weights['SAFE'] - 0.3) < 0.001
        assert abs(weights['GROWTH'] - 0.6) < 0.001
        assert 'CASH' in weights
