import pytest
from services.reits.sector_yield_tracker import SectorYieldTracker

def test_yield_attractiveness():
    svc = SectorYieldTracker()
    # Data Center: Benchmark 2.8%, Actual 4% -> HIGH spread
    res = svc.evaluate_yield("DLR", "DATA_CENTER", 0.04)
    assert res["attractiveness"] == "HIGH"
    assert res["yield_spread_bps"] == 120.0

def test_yield_neutral():
    svc = SectorYieldTracker()
    # Retail: Benchmark 5.2%, Actual 5.4% -> NEUTRAL
    res = svc.evaluate_yield("O", "RETAIL", 0.054)
    assert res["attractiveness"] == "NEUTRAL"
