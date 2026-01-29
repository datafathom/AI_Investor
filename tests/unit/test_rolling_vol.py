import pytest
from services.quantitative.rolling_volatility import RollingVolatilityEngine

def test_rolling_vol_window():
    svc = RollingVolatilityEngine()
    # 5 returns, window 3 -> 3 outputs.
    rets = [0.01, -0.01, 0.02, -0.02, 0.03]
    res = svc.calculate_rolling_vol(rets, window=3)
    assert len(res) == 3
    # All should be positive
    assert all(v > 0 for v in res)

def test_rolling_vol_insufficient():
    svc = RollingVolatilityEngine()
    assert svc.calculate_rolling_vol([0.1], window=5) == []
