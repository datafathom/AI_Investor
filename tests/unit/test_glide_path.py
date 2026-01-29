import pytest
from services.retirement.glide_path_engine import GlidePathEngine

def test_long_horizon_allocation():
    svc = GlidePathEngine()
    # 25 years -> 90% Equity
    res = svc.calculate_target_allocation(25)
    assert res["target_equity_pct"] == 0.90

def test_target_date_allocation():
    svc = GlidePathEngine()
    # 0 years -> 40% Equity
    res = svc.calculate_target_allocation(0)
    assert res["target_equity_pct"] == 0.40

def test_mid_horizon_shift():
    svc = GlidePathEngine()
    # 10 years -> 75% Equity
    res = svc.calculate_target_allocation(10)
    assert res["target_equity_pct"] == 0.75
