"""
Unit tests for Rule 144A Compliance API
Tests: Dashboard, Lockups, Holding Info, Sale Eligibility
"""

import pytest
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)


def test_compliance_dashboard():
    """Test compliance dashboard endpoint."""
    response = client.get("/api/v1/compliance/144a/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_restricted_positions" in data
    assert "max_quarterly_volume_pct" in data


def test_lockup_expirations():
    """Test lockup expirations list."""
    response = client.get("/api/v1/compliance/144a/lockups?days_ahead=90")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_holding_info():
    """Test holding info endpoint."""
    response = client.get("/api/v1/compliance/144a/holding/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert "status" in data


def test_sale_eligibility_check():
    """Test sale eligibility check."""
    response = client.post(
        "/api/v1/compliance/144a/check-sale",
        json={"ticker": "TSLA", "shares": 5000, "holder_id": "test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "TSLA"
    assert "can_sell" in data
