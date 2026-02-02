import pytest
from decimal import Decimal
from services.treasury.cash_management_service import CashManagementService

@pytest.fixture
def svc():
    return CashManagementService()

def test_calculate_sweep_yield(svc):
    amounts = {
        "CHECKING": Decimal("15000.00"),
        "MMA": Decimal("50000.00")
    }
    res = svc.calculate_sweep_yield(amounts)
    assert res["total_annual_return"] > 0
    assert res["optimal_move"] == "SWEEP_TO_T_BILL"

def test_simulate_treasury_ladder(svc):
    ladder = svc.simulate_treasury_ladder(Decimal("100000.00"), 6)
    assert len(ladder) == 6
    assert ladder[0]["amount"] == 100000.00 / 6
