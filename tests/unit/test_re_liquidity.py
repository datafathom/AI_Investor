import pytest
from services.real_estate.liquidity_model import RELiquidityModel

def test_reit_exit_costs():
    svc = RELiquidityModel()
    # 1M REIT -> $500 cost, 2 days
    res = svc.calculate_exit_costs("REIT", 1000000)
    assert res["exit_cost"] == 500.0
    assert res["days_to_cash"] == 2

def test_direct_exit_costs():
    svc = RELiquidityModel()
    # 1M Direct -> $80,000 cost, 90 days
    res = svc.calculate_exit_costs("DIRECT", 1000000)
    assert res["exit_cost"] == 80000.0
    assert res["days_to_cash"] == 90
