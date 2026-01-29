import pytest
from services.quantitative.volatility_analyzer import VolatilityAnalyzer

def test_standard_volatility():
    svc = VolatilityAnalyzer()
    # 1% daily vol approx 15.8% annual
    rets = [0.01, -0.01, 0.01, -0.01]
    res = svc.calculate_standard_vol(rets)
    assert 0.15 < res < 0.17

def test_downside_deviation():
    svc = VolatilityAnalyzer()
    # All returns positive -> 0 downside dev
    rets = [0.01, 0.02, 0.03]
    assert svc.calculate_downside_deviation(rets, 0.0) == 0.0
    
    # Mixed returns
    rets = [0.05, -0.05]
    res = svc.calculate_downside_deviation(rets, 0.0)
    assert res > 0
