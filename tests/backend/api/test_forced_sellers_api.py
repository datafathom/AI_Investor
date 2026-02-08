"""
Unit tests for Forced Sellers API
Tests: List risks, Heatmap, Traps, Ticker fragility
"""

import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)


def test_list_forced_seller_risks():
    """Test listing top fragile tickers."""
    response = client.get("/api/v1/market-data/forced-sellers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "ticker" in data[0]
        assert "fragility_score" in data[0]
        assert "risk_level" in data[0]


def test_get_passive_heatmap():
    """Test sector heatmap data."""
    response = client.get("/api/v1/market-data/forced-sellers/heatmap")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "sector" in data[0]
        assert "avg_passive_pct" in data[0]


def test_get_liquidity_traps():
    """Test liquidity trap detection endpoint."""
    response = client.get("/api/v1/market-data/forced-sellers/traps")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_ticker_fragility():
    """Test fragility score for a specific ticker."""
    response = client.get("/api/v1/market-data/forced-sellers/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "fragility_score" in data
    assert 0 <= data["fragility_score"] <= 100
