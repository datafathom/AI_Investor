import pytest
from services.quantitative.tracking_error import TrackingErrorCalculator

def test_zero_tracking_error():
    svc = TrackingErrorCalculator()
    # Identical returns
    rets = [0.01, -0.02, 0.05]
    assert svc.calculate_tracking_error(rets, rets) == 0.0

def test_tracking_error_presence():
    svc = TrackingErrorCalculator()
    # Different returns
    p_rets = [0.01, 0.02, 0.01]
    b_rets = [0.005, 0.025, 0.005]
    res = svc.calculate_tracking_error(p_rets, b_rets)
    assert res > 0
