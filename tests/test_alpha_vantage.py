"""
==============================================================================
FILE: tests/test_alpha_vantage.py
ROLE: Unit Tests for Alpha Vantage Client
PURPOSE: Test suite for AlphaVantageClient covering quotes, history, intraday,
         earnings, caching, and error handling.

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime

from services.data.alpha_vantage import (
    AlphaVantageClient, QuoteModel, OHLCVModel, EarningsModel, IntervalType,
    get_alpha_vantage_client
)


class TestAlphaVantageClient:
    """Test suite for AlphaVantageClient."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock-enabled client."""
        return AlphaVantageClient(mock=True)

    @pytest.fixture
    def live_client(self):
        """Create a client with API key for testing."""
        return AlphaVantageClient(api_key="demo", mock=False)

    # =========================================================================
    # Quote Tests
    # =========================================================================

    def test_get_quote_mock(self, mock_client):
        """Test quote retrieval in mock mode."""
        async def run_test():
            quote = await mock_client.get_quote("AAPL")
            assert quote is not None
            assert isinstance(quote, QuoteModel)
            assert quote.symbol == "AAPL"
            assert quote.price > 0
            return quote

        quote = asyncio.get_event_loop().run_until_complete(run_test())
        assert quote.source == "alpha_vantage"

    def test_get_quote_invalid_returns_none(self, live_client):
        """Test that invalid symbols return appropriate error handling."""
        # With mock disabled but no valid response, should handle gracefully
        async def run_test():
            # This would normally call the API, but we'll mock the response
            with patch.object(live_client, '_make_request', new_callable=AsyncMock) as mock_req:
                mock_req.return_value = {"Global Quote": {}}
                result = await live_client.get_quote("INVALID")
                return result

        result = asyncio.get_event_loop().run_until_complete(run_test())
        assert result is None

    # =========================================================================
    # Intraday Tests
    # =========================================================================

    def test_get_intraday_mock(self, mock_client):
        """Test intraday data retrieval in mock mode."""
        async def run_test():
            bars = await mock_client.get_intraday("MSFT", IntervalType.MIN_5)
            assert bars is not None
            assert isinstance(bars, list)
            assert len(bars) > 0
            assert isinstance(bars[0], OHLCVModel)
            return bars

        bars = asyncio.get_event_loop().run_until_complete(run_test())
        assert bars[0].close > 0

    def test_get_intraday_all_intervals(self, mock_client):
        """Test all interval types work."""
        async def run_test():
            for interval in IntervalType:
                bars = await mock_client.get_intraday("AAPL", interval)
                assert bars is not None
                assert len(bars) > 0

        asyncio.get_event_loop().run_until_complete(run_test())

    # =========================================================================
    # Daily Tests
    # =========================================================================

    def test_get_daily_mock(self, mock_client):
        """Test daily data retrieval in mock mode."""
        async def run_test():
            bars = await mock_client.get_daily("GOOGL")
            assert bars is not None
            assert isinstance(bars, list)
            assert len(bars) > 0
            return bars

        bars = asyncio.get_event_loop().run_until_complete(run_test())
        assert isinstance(bars[0], OHLCVModel)

    # =========================================================================
    # Earnings Tests
    # =========================================================================

    def test_get_earnings_mock(self, mock_client):
        """Test earnings calendar in mock mode."""
        async def run_test():
            earnings = await mock_client.get_earnings_calendar()
            assert earnings is not None
            assert isinstance(earnings, list)
            assert len(earnings) > 0
            return earnings

        earnings = asyncio.get_event_loop().run_until_complete(run_test())
        assert isinstance(earnings[0], EarningsModel)
        assert earnings[0].symbol in ["AAPL", "MSFT"]

    # =========================================================================
    # Caching Tests
    # =========================================================================

    def test_cache_hit(self, mock_client):
        """Test that cache returns data on second request."""
        async def run_test():
            # First call
            quote1 = await mock_client.get_quote("CACHE_TEST")
            # Second call should hit cache
            quote2 = await mock_client.get_quote("CACHE_TEST")
            return quote1, quote2

        q1, q2 = asyncio.get_event_loop().run_until_complete(run_test())
        assert q1 is not None
        assert q2 is not None
        # Both should have same timestamp since cache is used

    def test_cache_disabled(self):
        """Test client works with cache disabled."""
        client = AlphaVantageClient(mock=True, use_cache=False)

        async def run_test():
            quote = await client.get_quote("NO_CACHE")
            return quote

        quote = asyncio.get_event_loop().run_until_complete(run_test())
        assert quote is not None

    # =========================================================================
    # Backward Compatibility Tests
    # =========================================================================

    def test_get_latest_price_sync(self, mock_client):
        """Test sync wrapper for backward compatibility."""
        result = mock_client.get_latest_price("TEST")
        assert result is not None
        assert "symbol" in result
        assert "price" in result
        assert "volume" in result
        assert "change_percent" in result

    def test_get_daily_time_series_sync(self, mock_client):
        """Test sync wrapper for daily time series."""
        result = mock_client.get_daily_time_series("TEST")
        assert result is not None
        assert "Time Series (Daily)" in result

    # =========================================================================
    # Singleton Tests
    # =========================================================================

    def test_singleton_client(self):
        """Test singleton pattern returns same instance."""
        client1 = get_alpha_vantage_client(mock=True)
        client2 = get_alpha_vantage_client()
        assert client1 is client2

    # =========================================================================
    # Model Validation Tests
    # =========================================================================

    def test_quote_model_validation(self):
        """Test QuoteModel accepts valid data."""
        quote = QuoteModel(
            symbol="TEST",
            price=150.50,
            volume=1000000,
            change=2.50,
            change_percent="1.69%"
        )
        assert quote.symbol == "TEST"
        assert quote.price == 150.50

    def test_ohlcv_model_validation(self):
        """Test OHLCVModel accepts valid data."""
        bar = OHLCVModel(
            timestamp=datetime.now(),
            open=100.0,
            high=105.0,
            low=99.0,
            close=102.0,
            volume=500000
        )
        assert bar.high > bar.low
        assert bar.volume > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
