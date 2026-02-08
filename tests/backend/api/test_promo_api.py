"""
Unit tests for Volume Promo API
Tests: Promo Spikes, Volume Baseline, Promo History
"""

import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)


def test_get_promo_spikes():
    """Test promo spike detection endpoint."""
    response = client.get("/api/v1/market-data/promo-spikes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "ticker" in data[0]
        assert "is_promo_spike" in data[0]
        assert "volume_ratio" in data[0]


def test_get_volume_baseline():
    """Test volume baseline endpoint."""
    response = client.get("/api/v1/market-data/promo-spikes/baseline/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "avg_4_week_volume" in data


def test_get_promo_history():
    """Test promo history endpoint."""
    response = client.get("/api/v1/market-data/promo-spikes/history/TSLA")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
