import pytest
from services.planning.target_adjuster import TargetReturnAdjuster

def test_nominal_adjustment():
    svc = TargetReturnAdjuster()
    # 5% real, 3% inflation -> 8.15% nominal
    res = svc.adjust_target(0.05, 0.03)
    assert res == 0.0815

def test_zero_inflation_adjustment():
    svc = TargetReturnAdjuster()
    assert svc.adjust_target(0.07, 0.0) == 0.07
