
import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import MagicMock, patch
from services.analysis.prediction_service import PredictionService

@pytest.fixture
def mock_df():
    # Create a synthetic dataframe with a clear pattern
    # If RSI is high (simulated by high close), returns are negative (Mean Reversion)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='1D')
    df = pd.DataFrame(index=dates)
    df['open'] = 100.0
    df['high'] = 105.0
    df['low'] = 95.0
    df['close'] = np.sin(np.linspace(0, 10, 100)) * 10 + 100
    df['volume'] = 1000
    return df

class TestPredictionService:
    
    def test_initialization(self):
        service = PredictionService()
        assert service.feature_service is not None

    def test_train_model_logic(self, mock_df):
        """
        Logical Test: Verify that training produces a model and returns metrics.
        """
        service = PredictionService()
        
        # We need to mock XGBoost if not installed, but here we assume it enters the test 
        # phase after installation. 
        # If imports fail in service, this test will fail, which is good.
        
        metrics = service.train_model(mock_df)
        
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert service.model is not None
        assert os.path.exists(service.model_path)
        
    def test_predict_direction(self, mock_df):
        """
        Logical Test: Verify prediction returns valid structure.
        """
        service = PredictionService()
        
        # Train first
        service.train_model(mock_df)
        
        # Predict
        result = service.predict_direction(mock_df)
        
        assert "prediction" in result
        assert result["prediction"] in ["UP", "DOWN"]
        assert "probability_up" in result
        assert 0 <= result["probability_up"] <= 1.0

    def test_insufficient_data(self):
        service = PredictionService()
        tiny_df = pd.DataFrame({'close': [100, 101]}) # Too small for windows
        
        with pytest.raises(Exception): # ValueError or KeyError from feature service/training
            service.train_model(tiny_df)
