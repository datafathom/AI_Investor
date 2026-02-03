"""
==============================================================================
FILE: tests/test_polygon_integration.py
ROLE: Unit Tests for Polygon and Data Fusion Failover
PURPOSE: Verifies PolygonService data retrieval and DataFusionService's 
         ability to failover when primary source is unavailable.

AUTHOR: AI Investor Team
CREATED: 2026-01-22
==============================================================================
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime

from services.data.polygon_service import PolygonService, AggregateBar
from services.data.data_fusion_service import DataFusionService


class TestPolygonIntegration:
    """Test suite for Polygon and Failover logic."""

    @pytest.fixture
    def polygon_service(self):
        return PolygonService(mock=True)

    @pytest.fixture
    def fusion_service(self):
        return DataFusionService(mock=True)

    # =========================================================================
    # Polygon Service Tests
    # =========================================================================

    def test_polygon_mock_aggregates(self, polygon_service):
        """Test aggregate retrieval in mock mode."""
        async def run_test():
            bars = await polygon_service.get_aggregates("AAPL", limit=5)
            assert len(bars) == 5
            assert isinstance(bars[0], AggregateBar)
            assert bars[0].close > 0
            return bars

        asyncio.run(run_test())

    def test_polygon_get_latest_price_mock(self, polygon_service):
        """Test latest price interface."""
        data = polygon_service.get_latest_price("AAPL")
        assert data is not None
        assert data["symbol"] == "AAPL"
        assert "price" in data
        assert data["source"] == "polygon_mock"

    # =========================================================================
    # Data Fusion Failover Tests
    # =========================================================================

    def test_fusion_failover_to_polygon(self, fusion_service):
        """Test that fusion service falls back to polygon when primary fails."""
        # Mock primary service to return None
        fusion_service.primary_price_service.get_latest_price = MagicMock(return_value=None)
        
        # Mock secondary service to return valid data
        fusion_service.secondary_price_service.get_latest_price = MagicMock(return_value={
            "symbol": "TSLA",
            "price": 250.0,
            "volume": 5000000,
            "change_percent": 2.5,
            "source": "polygon_test"
        })

        tensor = fusion_service.get_market_state_tensor("TSLA")
        
        assert tensor["data_source"] == "polygon"
        assert tensor["tensor"]["price_momentum"] > 0
        assert tensor["aggregate_score"] > 0

    def test_fusion_primary_success(self, fusion_service):
        """Test that fusion service uses primary when available."""
        fusion_service.primary_price_service.get_latest_price = MagicMock(return_value={
            "symbol": "TSLA",
            "price": 240.0,
            "volume": 4000000,
            "change_percent": 1.5,
            "source": "alpha_vantage_test"
        })

        tensor = fusion_service.get_market_state_tensor("TSLA")
        
        assert tensor["data_source"] == "alpha_vantage"
        assert tensor["tensor"]["price_momentum"] > 0

    def test_fusion_complete_failure(self, fusion_service):
        """Test behavior when both services fail."""
        fusion_service.primary_price_service.get_latest_price = MagicMock(return_value=None)
        fusion_service.secondary_price_service.get_latest_price = MagicMock(return_value=None)

        tensor = fusion_service.get_market_state_tensor("TSLA")
        
        assert tensor["data_source"] == "none"
        assert tensor["status"] == "QUARANTINED"
        assert "Invalid or stale price data" in tensor["quarantine_reasons"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
