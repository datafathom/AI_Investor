import pytest
from services.risk.geopolitical_risk_svc import GeopoliticalRiskService

@pytest.fixture
def svc():
    return GeopoliticalRiskService()

def test_simulate_total_war(svc):
    allocation = {"Equities": 0.5, "Gold": 0.5}
    res = svc.simulate_total_war(allocation)
    
    assert "scenario" in res
    assert -1.0 <= res["total_portfolio_impact"] <= 1.0
    assert "Equities" in res["asset_breakdown"]
    assert "Gold" in res["asset_breakdown"]

def test_calculate_geopolitical_fear_score(svc):
    # Case: Extreme fear
    res = svc.calculate_geopolitical_fear_score(45.0, 1.8, 0.1)
    assert res["fear_score"] > 0.8
    assert res["is_fear_overbid"] is True
    assert res["recommendation"] == "BET_AGAINST_FEAR"

    # Case: Low fear
    res2 = svc.calculate_geopolitical_fear_score(15.0, 0.8, 0.7)
    assert res2["fear_score"] < 0.5
    assert res2["is_fear_overbid"] is False
    assert res2["recommendation"] == "MAINTAIN_HEDGES"
