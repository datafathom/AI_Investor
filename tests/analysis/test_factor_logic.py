
import pytest
import pandas as pd
import numpy as np
from services.analysis.factor_service import FactorService

class TestFactorService:
    
    def test_calculate_factors(self):
        service = FactorService()
        dates = pd.date_range(start='2024-01-01', periods=50)
        df = pd.DataFrame(index=dates)
        # Rising price -> Positive Momentum
        df['close'] = np.linspace(100, 110, 50) 
        
        result = service.calculate_factors(df, window=10)
        
        assert 'volatility' in result.columns
        assert 'momentum' in result.columns
        # Last momentum should be positive (110 - ~108) / ~108
        assert result['momentum'].iloc[-1] > 0

    def test_risk_parity_weights(self):
        """
        Test that higher volatility results in lower weight.
        """
        service = FactorService()
        
        # Asset A: High Vol (0.2)
        # Asset B: Low Vol (0.1)
        # Expected: B should have 2x weight of A.
        # InvA = 5, InvB = 10. Total = 15.
        # Wa = 5/15 = 0.33
        # Wb = 10/15 = 0.66
        
        vols = {'A': 0.2, 'B': 0.1}
        weights = service.calculate_risk_parity_weights(vols)
        
        assert weights['B'] > weights['A']
        assert abs(weights['A'] - 0.333) < 0.01
        assert abs(weights['B'] - 0.666) < 0.01
        assert abs(sum(weights.values()) - 1.0) < 0.0001
        
    def test_zero_volatility_handling(self):
        service = FactorService()
        vols = {'A': 0.0, 'B': 0.1}
        weights = service.calculate_risk_parity_weights(vols)
        
        # A should be skipped or handled gracefully
        assert 'A' not in weights
        assert weights['B'] == 1.0

    def test_get_portfolio_weights_integration(self):
        service = FactorService()
        
        # Create DataFrames
        df_a = pd.DataFrame({'close': np.random.randn(100) * 2 + 100}) # High noise
        df_b = pd.DataFrame({'close': np.random.randn(100) * 0.5 + 100}) # Low noise
        
        prices = {'HighVol': df_a, 'LowVol': df_b}
        
        weights = service.get_portfolio_weights(prices)
        
        assert 'LowVol' in weights
        assert 'HighVol' in weights
        assert weights['LowVol'] > weights['HighVol']
