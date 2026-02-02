import pytest
from decimal import Decimal
from services.tax.tax_harvest_service import TaxHarvestService

@pytest.fixture
def svc():
    return TaxHarvestService()

def test_hunt_harvest_opportunity(svc):
    portfolio = [
        {"ticker": "ABC", "cost_basis": 100.0, "current_price": 85.0}, # 15% loss
        {"ticker": "XYZ", "cost_basis": 100.0, "current_price": 95.0}  # 5% loss
    ]
    opps = svc.hunt_harvest_opportunity(portfolio)
    assert len(opps) == 1
    assert opps[0]["ticker"] == "ABC"
    assert opps[0]["loss_pct"] == 15.0

def test_optimize_carryforward(svc):
    res = svc.optimize_carryforward(Decimal("5000.00"), Decimal("7000.00"))
    assert res["taxable_net"] == 0
    assert res["unused_loss_carryforward"] == Decimal("2000.00")
    assert res["tax_efficiency"] == "OPTIMAL"
