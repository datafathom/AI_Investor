"""
Tests for Technical Analysis Service
Comprehensive test coverage for technical indicators and pattern recognition
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import pandas as pd
import numpy as np
from services.analysis.technical_analysis_service import TechnicalAnalysisService


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.analysis.technical_analysis_service.FeatureEngineeringService') as MockService:
        mock_instance = MockService.return_value
        
        # Configure RSI mock
        mock_instance._calculate_rsi.return_value = {'rsi': pd.Series([50.0] * 100)}
        
        # Configure MACD mock
        mock_instance._calculate_macd.return_value = pd.DataFrame({
            'macd': [0.5] * 100,
            'macd_signal': [0.4] * 100,
            'macd_hist': [0.1] * 100
        })
        
        # Configure Bollinger mock
        mock_instance._calculate_bollinger_bands.return_value = pd.DataFrame({
            'upper': [155.0] * 100,
            'middle': [150.0] * 100,
            'lower': [145.0] * 100
        })
        
        return TechnicalAnalysisService()


@pytest.fixture
def mock_ohlcv_data():
    """Mock OHLCV data."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'open': np.random.uniform(145, 155, 100),
        'high': np.random.uniform(150, 160, 100),
        'low': np.random.uniform(140, 150, 100),
        'close': np.random.uniform(145, 155, 100),
        'volume': np.random.uniform(1000000, 2000000, 100)
    }, index=dates)


@pytest.mark.asyncio
async def test_calculate_indicators_rsi(service, mock_ohlcv_data):
    """Test RSI indicator calculation."""
    result = await service.calculate_indicators(mock_ohlcv_data, ['RSI'])
    
    assert result is not None
    assert 'RSI' in result
    assert isinstance(result['RSI'], pd.Series)


@pytest.mark.asyncio
async def test_calculate_indicators_macd(service, mock_ohlcv_data):
    """Test MACD indicator calculation."""
    result = await service.calculate_indicators(mock_ohlcv_data, ['MACD'])
    
    assert result is not None
    assert 'MACD' in result


@pytest.mark.asyncio
async def test_calculate_indicators_bollinger(service, mock_ohlcv_data):
    """Test Bollinger Bands calculation."""
    result = await service.calculate_indicators(mock_ohlcv_data, ['BB'])
    
    assert result is not None
    assert 'Bollinger' in result


@pytest.mark.asyncio
async def test_calculate_indicators_multiple(service, mock_ohlcv_data):
    """Test calculating multiple indicators."""
    result = await service.calculate_indicators(
        mock_ohlcv_data,
        ['RSI', 'MACD', 'SMA_20', 'EMA_50']
    )
    
    assert result is not None
    assert len(result) == 4


@pytest.mark.asyncio
async def test_recognize_patterns(service, mock_ohlcv_data):
    """Test pattern recognition."""
    result = await service.recognize_patterns(mock_ohlcv_data)
    
    assert result is not None
    assert isinstance(result, list) or isinstance(result, dict)


@pytest.mark.asyncio
async def test_generate_trading_signals(service, mock_ohlcv_data):
    """Test trading signal generation."""
    service.calculate_indicators = AsyncMock(return_value={
        'RSI': pd.Series([25.0] * 100),  # Oversold (< 30)
        'MACD': pd.DataFrame({
            'macd': [0.6] * 100,
            'macd_signal': [0.5] * 100
        }),
        'SMA_50': pd.Series([150.0] * 100),
        'SMA_200': pd.Series([140.0] * 100) # Gold cross condition
    })
    
    result = await service.generate_trading_signals(mock_ohlcv_data)
    
    assert result is not None
    assert isinstance(result, list) or isinstance(result, dict)
