import pytest
from services.quantitative.rolling_metrics import RollingMetricsEngine

def test_sharpe_calculation():
    svc = RollingMetricsEngine()
    # 252 returns of 0.01% daily (approx 2.5% annual), Rf=0 -> Sharpe constant
    rets = [0.0001] * 252*3
    res = svc.calculate_rolling_sharpe(rets, 0.0, window=252*3)
    assert len(res) == 1
    assert res[0] > 0

def test_sortino_downside_only():
    svc = RollingMetricsEngine()
    # Big positive moves shouldn't hurt Sortino much, but Sharpe would be lower
    rets = [0.01, -0.01, 0.05, -0.01, 0.01]
    sortino = svc.calculate_sortino(rets, 0.0)
    assert sortino != 0
