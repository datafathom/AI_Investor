import pytest
from services.market_data.forced_seller_svc import ForcedSellerService

@pytest.fixture
def svc():
    return ForcedSellerService()

def test_monitor_passive_flow(svc):
    # Normal flow
    res = svc.monitor_passive_flow("AAPL", 25.0)
    assert res["fragility_score"] == 0.25
    assert res["risk_level"] == "LOW"

    # Extreme flow
    res2 = svc.monitor_passive_flow("QQQ", 85.0)
    assert res2["fragility_score"] == 0.85
    assert res2["risk_level"] == "CRITICAL"

def test_detect_liquidity_trap(svc):
    res = svc.detect_liquidity_trap(0.20, 0.05) # 4x expansion
    assert res["is_liquidity_trap"] is True
    assert res["severity"] == "HIGH"
    assert res["action"] == "HALT_ACTIVE_TRADING"
