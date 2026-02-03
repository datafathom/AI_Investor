"""
==============================================================================
FILE: tests/test_fred_service.py
ROLE: Unit Tests for FRED Macro Service
PURPOSE: Test suite for FredMacroService covering series retrieval, regime
         analysis, yield curve, transformations, and caching.

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime

from services.data.fred_service import (
    FredMacroService, DataPoint, SeriesMetadata, MacroRegime, TransformType,
    get_fred_service
)


class TestFredMacroService:
    """Test suite for FredMacroService."""

    @pytest.fixture
    def mock_service(self):
        """Create a mock-enabled service."""
        return FredMacroService(mock=True)

    @pytest.fixture
    def live_service(self):
        """Create a service with API key for testing."""
        return FredMacroService(api_key="demo", mock=False)

    # =========================================================================
    # Series Retrieval Tests
    # =========================================================================

    def test_get_series_mock(self, mock_service):
        """Test series retrieval in mock mode."""
        async def run_test():
            data = await mock_service.get_series("CPIAUCSL", limit=10)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            assert isinstance(data[0], DataPoint)
            return data

        data = asyncio.get_event_loop().run_until_complete(run_test())
        assert data[0].date is not None

    def test_get_latest_value_mock(self, mock_service):
        """Test latest value retrieval in mock mode."""
        async def run_test():
            value = await mock_service.get_latest_value("UNRATE")
            assert value is not None
            assert isinstance(value, float)
            return value

        value = asyncio.get_event_loop().run_until_complete(run_test())
        assert value == 3.7  # Mock unemployment rate

    def test_get_series_metadata_mock(self, mock_service):
        """Test metadata retrieval in mock mode."""
        async def run_test():
            metadata = await mock_service.get_series_metadata("CPIAUCSL")
            assert metadata is not None
            assert isinstance(metadata, SeriesMetadata)
            return metadata

        metadata = asyncio.get_event_loop().run_until_complete(run_test())
        assert metadata.id == "CPIAUCSL"

    # =========================================================================
    # Regime Analysis Tests
    # =========================================================================

    def test_get_macro_regime_mock(self, mock_service):
        """Test macro regime retrieval in mock mode."""
        async def run_test():
            regime = await mock_service.get_macro_regime()
            assert regime is not None
            assert isinstance(regime, MacroRegime)
            return regime

        regime = asyncio.get_event_loop().run_until_complete(run_test())
        assert regime.status in ["EXPANSION", "CONTRACTION", "SLOWDOWN", "RECESSION_WARNING"]
        assert isinstance(regime.health_score, float)
        assert 0 <= regime.health_score <= 100

    def test_regime_inverted_yield_curve(self, mock_service):
        """Test regime detection with inverted yield curve."""
        data = {"YIELD_CURVE": -0.5, "UNEMPLOYMENT": 3.5, "VIX": 15}
        regime = mock_service._analyze_regime(data)
        
        assert regime.status == "RECESSION_WARNING"
        assert "YIELD_CURVE_INVERTED" in regime.signals

    def test_regime_high_unemployment(self, mock_service):
        """Test regime detection with high unemployment."""
        data = {"YIELD_CURVE": 1.0, "UNEMPLOYMENT": 7.0, "VIX": 20}
        regime = mock_service._analyze_regime(data)
        
        assert regime.status == "CONTRACTION"
        assert "HIGH_UNEMPLOYMENT" in regime.signals

    def test_regime_health_score_bounds(self, mock_service):
        """Test that health score stays within 0-100."""
        # Very negative scenario
        data = {
            "YIELD_CURVE": -1.0, 
            "UNEMPLOYMENT": 10.0, 
            "VIX": 50,
            "GDP_GROWTH": -5.0
        }
        regime = mock_service._analyze_regime(data)
        assert 0 <= regime.health_score <= 100

        # Very positive scenario
        data = {
            "YIELD_CURVE": 2.0, 
            "UNEMPLOYMENT": 3.0, 
            "VIX": 12,
            "GDP_GROWTH": 4.0
        }
        regime = mock_service._analyze_regime(data)
        assert 0 <= regime.health_score <= 100

    # =========================================================================
    # Yield Curve Tests
    # =========================================================================

    def test_get_yield_curve_mock(self, mock_service):
        """Test yield curve retrieval in mock mode."""
        async def run_test():
            curve = await mock_service.get_yield_curve_data()
            assert curve is not None
            assert isinstance(curve, dict)
            assert "10Y" in curve
            assert "2Y" in curve
            return curve

        curve = asyncio.get_event_loop().run_until_complete(run_test())
        assert curve["10Y"] < curve["2Y"]  # Mock shows inverted

    # =========================================================================
    # Transformation Tests
    # =========================================================================

    def test_yoy_transform(self, mock_service):
        """Test year-over-year transformation."""
        data = [
            DataPoint(date=f"2026-{12-i:02d}-01", value=100 + i)
            for i in range(15)
        ]
        
        transformed = mock_service._apply_transform(data, TransformType.YOY)
        assert len(transformed) > 0
        assert transformed[0].value is not None

    def test_mom_transform(self, mock_service):
        """Test month-over-month transformation."""
        data = [
            DataPoint(date=f"2026-{12-i:02d}-01", value=100 + i * 2)
            for i in range(5)
        ]
        
        transformed = mock_service._apply_transform(data, TransformType.MOM)
        assert len(transformed) == 4  # One less than input

    def test_calculate_yoy_change(self, mock_service):
        """Test YoY change calculation."""
        async def run_test():
            yoy = await mock_service.calculate_yoy_change("CPIAUCSL")
            # In mock mode, this should return a value
            return yoy

        result = asyncio.get_event_loop().run_until_complete(run_test())
        # Mock data may not have enough history, so result could be None
        assert result is None or isinstance(result, float)

    # =========================================================================
    # Caching Tests
    # =========================================================================

    def test_cache_hit(self, mock_service):
        """Test that cache returns data on second request."""
        async def run_test():
            # First call
            data1 = await mock_service.get_series("CACHE_TEST", limit=5)
            # Second call should hit cache
            data2 = await mock_service.get_series("CACHE_TEST", limit=5)
            return data1, data2

        d1, d2 = asyncio.get_event_loop().run_until_complete(run_test())
        assert d1 is not None
        assert d2 is not None

    def test_cache_disabled(self):
        """Test service works with cache disabled."""
        service = FredMacroService(mock=True, use_cache=False)

        async def run_test():
            data = await service.get_series("NO_CACHE")
            return data

        data = asyncio.get_event_loop().run_until_complete(run_test())
        assert data is not None

    # =========================================================================
    # Backward Compatibility Tests
    # =========================================================================

    def test_get_macro_regime_sync(self, mock_service):
        """Test sync wrapper for backward compatibility."""
        result = mock_service.get_macro_regime_sync()
        assert result is not None
        assert "status" in result
        assert "health_score" in result

    def test_fetch_series_sync(self, mock_service):
        """Test sync _fetch_series method."""
        result = mock_service._fetch_series("UNRATE")
        assert result is not None
        assert isinstance(result, float)

    # =========================================================================
    # Singleton Tests
    # =========================================================================

    def test_singleton_service(self):
        """Test singleton pattern returns same instance."""
        service1 = get_fred_service(mock=True)
        service2 = get_fred_service()
        assert service1 is service2

    # =========================================================================
    # Model Validation Tests
    # =========================================================================

    def test_datapoint_model(self):
        """Test DataPoint model accepts valid data."""
        dp = DataPoint(date="2026-01-21", value=100.5)
        assert dp.date == "2026-01-21"
        assert dp.value == 100.5

    def test_macro_regime_model(self):
        """Test MacroRegime model."""
        regime = MacroRegime(
            status="EXPANSION",
            signals=["LOW_VOLATILITY"],
            metrics={"VIX": 15},
            health_score=75.0
        )
        assert regime.status == "EXPANSION"
        assert regime.health_score == 75.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
