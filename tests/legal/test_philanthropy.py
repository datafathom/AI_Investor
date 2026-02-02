import pytest
from decimal import Decimal
from services.legal.philanthropy_service import PhilanthropyService

@pytest.fixture
def svc():
    return PhilanthropyService()

def test_calculate_charitable_deduction(svc):
    # Cash donation, under limit
    res = svc.calculate_charitable_deduction(Decimal("10000.00"), Decimal("100000.00"), "CASH")
    assert res["deductible_this_year"] == Decimal("10000.00")
    assert res["carryover_amount"] == 0
    
    # Large donation, over limit
    res2 = svc.calculate_charitable_deduction(Decimal("70000.00"), Decimal("100000.00"), "CASH")
    assert res2["deductible_this_year"] == Decimal("60000.00")
    assert res2["carryover_amount"] == Decimal("10000.00")

def test_score_social_impact(svc):
    donations = [{"amount": 50000, "efficacy": 1.0}]
    res = svc.score_social_impact(donations)
    assert res["social_id_score"] == 0.5 # 50000 / 100000
    assert res["tier"] == "CONTRIBUTOR"
