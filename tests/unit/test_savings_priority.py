import pytest
from services.planning.savings_priority import SavingsPriorityEngine

def test_ef_replenishment_priority():
    svc = SavingsPriorityEngine()
    # Need 10k, have 5k. Incoming 3k.
    # All 3k should go to EF.
    res = svc.prioritize_allocation(3000, 5000, 10000)
    assert res["emergency_fund_allocation"] == 3000.0
    assert res["investment_allocation"] == 0.0

def test_spillover_to_investments():
    svc = SavingsPriorityEngine()
    # Need 10k, have 9k. Incoming 5k.
    # 1k to EF, 4k to Invest.
    res = svc.prioritize_allocation(5000, 9000, 10000)
    assert res["emergency_fund_allocation"] == 1000.0
    assert res["investment_allocation"] == 4000.0
