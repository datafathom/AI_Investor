import pytest
from decimal import Decimal
from services.trading.option_hedge_service import OptionHedgeService

@pytest.fixture
def svc():
    return OptionHedgeService()

def test_recommend_hedge(svc):
    # Low Vol -> Collar
    res = svc.recommend_hedge("NVDA", 120.0, 12.0, Decimal("200000.00"))
    assert res["strategy"] == "PUT_COLLAR"
    assert res["strikes"]["put"] == 114.0
    assert res["strikes"]["call"] == 132.0

    # High Vol -> VIX Calls
    res2 = svc.recommend_hedge("NVDA", 120.0, 45.0, Decimal("10000.00"))
    assert res2["strategy"] == "VIX_CALLS"

def test_calculate_tax_shield(svc):
    res = svc.calculate_tax_shield(Decimal("1000.00"), Decimal("5000.00"))
    assert res["net_benefit"] == Decimal("4000.00")
    assert res["efficiency_pct"] == 80.0
