import pytest
from services.quantitative.weighting_comparator import WeightingComparator

def test_breadth_analysis():
    svc = WeightingComparator()
    # Narrow Market: Big stocks (CW) lead
    cw = [0.05, 0.10, 0.15]
    ew = [0.01, 0.02, 0.03]
    res = svc.compare_performance(cw, ew)
    assert res["market_breadth"] == "NARROW_LEADERSHIP"
    assert res["spread"] < 0

def test_healthy_breadth():
    svc = WeightingComparator()
    # Healthy Market: Small stocks (EW) lead
    cw = [0.01, 0.02]
    ew = [0.05, 0.06]
    res = svc.compare_performance(cw, ew)
    assert res["market_breadth"] == "HEALTHY"
    assert res["spread"] > 0
