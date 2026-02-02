import pytest
from services.risk.commodity_tracker import CommodityExposureTracker

@pytest.fixture
def tracker():
    return CommodityExposureTracker()

def test_get_em_vulnerability(tracker):
    # Saudi Arabia Oil shock
    res = tracker.get_em_vulnerability("SAUDI_ARABIA", ["Oil"])
    assert res["vulnerability_score"] == 0.5 # 1 of 2
    assert res["impact_severity"] == "LOW" # 0.5 is not > 0.5

    # Chile Copper shock
    res2 = tracker.get_em_vulnerability("CHILE", ["Copper"])
    assert res2["vulnerability_score"] == 1.0
    assert res2["impact_severity"] == "HIGH"

def test_list_at_risk_countries(tracker):
    res = tracker.list_at_risk_countries("Oil Price Spike")
    assert "SAUDI_ARABIA" in res
    assert "BRAZIL" in res
    
    res2 = tracker.list_at_risk_countries("Copper Shortage")
    assert "CHILE" in res2
