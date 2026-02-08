"""
Unit tests for Whale Flow API
Tests: Summary, Filings, Crowding, Holder Details, Ticker Activity
"""

import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)


def test_whale_flow_summary():
    """Test whale flow summary endpoint."""
    response = client.get("/api/v1/market-data/whale-flow")
    assert response.status_code == 200
    data = response.json()
    assert "total_filings_this_quarter" in data
    assert "net_buying_billions" in data


def test_recent_filings():
    """Test recent 13F filings list."""
    response = client.get("/api/v1/market-data/whale-flow/filings?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_sector_crowding():
    """Test sector crowding analysis."""
    response = client.get("/api/v1/market-data/whale-flow/crowding")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "sector" in data[0]
        assert "crowding_score" in data[0]


def test_holder_details():
    """Test holder details endpoint."""
    response = client.get("/api/v1/market-data/whale-flow/holders/BlackRock")
    assert response.status_code == 200
    data = response.json()
    assert "holder_name" in data
    assert data["holder_name"] == "BlackRock"


def test_ticker_whale_activity():
    """Test ticker whale activity."""
    response = client.get("/api/v1/market-data/whale-flow/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert "ticker" in data
    assert data["ticker"] == "AAPL"
    assert "holders" in data
