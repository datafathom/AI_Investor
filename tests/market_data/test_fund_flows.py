import pytest
from services.market_data.fund_flow_service import FundFlowService

@pytest.fixture
def svc():
    return FundFlowService()

def test_track_whale_selling(svc):
    data = [
        {"holder": "Whale A", "change": -2000000},
        {"holder": "Whale B", "change": 1000000},
        {"holder": "Whale C", "change": -5000000}
    ]
    res = svc.track_whale_selling("NVDA", data)
    assert res["total_whale_sold"] == 7000000
    assert len(res["major_sellers"]) == 2
    assert res["risk_level"] == "ELEVATED"

def test_detect_sector_overcrowding(svc):
    res = svc.detect_sector_overcrowding("TECH", 0.9)
    assert res["is_overcrowded"] is True
    assert res["action"] == "TRIM_EXPOSURE"
