import pytest
from services.risk.indirect_leverage import IndirectLeverageCalculator

def test_safe_leverage():
    svc = IndirectLeverageCalculator()
    # 100k equity, 150k exposure -> 1.5x
    res = svc.calculate_true_leverage(100000, 100000, 50000, 0)
    assert res["leverage_ratio"] == 1.5
    assert res["status"] == "SAFE"

def test_critical_leverage():
    svc = IndirectLeverageCalculator()
    # 100k equity, 350k exposure -> 3.5x
    res = svc.calculate_true_leverage(100000, 100000, 250000, 0)
    assert res["leverage_ratio"] == 3.5
    assert res["status"] == "CRITICAL"
