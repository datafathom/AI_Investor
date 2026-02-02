import pytest
from decimal import Decimal
from services.alternative.pe_secondary_service import PESecondaryService

@pytest.fixture
def svc():
    return PESecondaryService()

def test_calculate_nav_discount(svc):
    res = svc.calculate_nav_discount(Decimal("1000.00"), Decimal("600.00"))
    assert res["discount_pct"] == 40.0
    assert res["opportunity_rank"] == "HIGH"

def test_track_redemption_window(svc):
    res = svc.track_redemption_window("FUND_X", "2026-06-30")
    assert res["fund_id"] == "FUND_X"
    assert "lockup_expiry" in res
