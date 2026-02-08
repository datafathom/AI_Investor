"""
Unit tests for Technical Indicators API
Tests: List indicators, Details, Calculate, Custom
"""

import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)


def test_list_indicators():
    """Test list all indicators."""
    response = client.get("/api/v1/indicators")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 10  # At least 10 built-in indicators


def test_get_indicator_details():
    """Test get indicator details."""
    response = client.get("/api/v1/indicators/rsi")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "rsi"
    assert "params" in data


def test_calculate_indicator():
    """Test calculate indicator endpoint."""
    response = client.post(
        "/api/v1/indicators/calculate",
        json={"ticker": "AAPL", "indicator": "sma", "params": {"period": 20}, "period": "1M"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["indicator"] == "sma"
    assert "values" in data


def test_indicator_not_found():
    """Test 404 for unknown indicator."""
    response = client.get("/api/v1/indicators/nonexistent")
    assert response.status_code == 404
