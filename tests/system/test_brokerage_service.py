import pytest
from services.brokerage.brokerage_service import get_brokerage_service

def test_brokerage_service_singleton():
    s1 = get_brokerage_service()
    s2 = get_brokerage_service()
    assert s1 is s2

def test_get_status_simulated():
    service = get_brokerage_service()
    service.is_simulated = True
    status = service.get_status()
    assert "summary" in status
    assert "connections" in status
    assert any(c["name"] == "Alpaca-Sandbox" for c in status["connections"])
    assert status["total_buying_power"] > 0

def test_get_positions_simulated():
    service = get_brokerage_service()
    service.is_simulated = True
    positions = service.get_positions()
    assert len(positions) >= 3
    assert any(p["symbol"] == "AAPL" for p in positions)
    assert "market_value" in positions[0]

def test_connection_invalid_keys():
    service = get_brokerage_service()
    # This should fail validation if alpaca-trade-api is present, 
    # or just return False if we can't connect.
    success = service.connect_with_keys("invalid", "invalid")
    assert success is False
