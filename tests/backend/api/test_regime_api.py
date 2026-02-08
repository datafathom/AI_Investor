"""
Unit tests for Market Regime API
Tests: Current Regime, History, Forecast
"""

import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)


def test_get_current_regime():
    """Test get current market regime."""
    response = client.get("/api/v1/market/regime")
    assert response.status_code == 200
    data = response.json()
    assert "regime" in data
    assert "confidence" in data
    assert "indicators" in data
    assert isinstance(data["indicators"], list)


def test_get_regime_history():
    """Test get historical regimes."""
    response = client.get("/api/v1/market/regime/history?days=30")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "regime" in data[0]
        assert "date" in data[0]


def test_get_regime_forecast():
    """Test get regime forecast."""
    response = client.get("/api/v1/market/regime/forecast")
    assert response.status_code == 200
    data = response.json()
    assert "forecast_regime" in data
    assert "probability" in data
