import pytest
from services.quantitative.sharpe_calculator import SharpeRatioCalculator

def test_sharpe_basic():
    svc = SharpeRatioCalculator()
    # 0.1% daily return approx 25% annual.
    # Sigma daily 1% approx 16% annual.
    # (0.25 - 0.05) / 0.16 = 1.25
    rets = [0.001] * 100
    res = svc.calculate(rets, 0.05)
    assert res > 1.0

def test_sharpe_zero_vol():
    svc = SharpeRatioCalculator()
    assert svc.calculate([0, 0, 0], 0.05) == 0.0

def test_negative_sharpe():
    svc = SharpeRatioCalculator()
    # Mean -0.1% daily with variance
    rets = [-0.001, -0.002, 0.0, -0.0015] * 20
    res = svc.calculate(rets, 0.05)
    assert res < 0
