import pytest
from services.banking.sweep_tracker import SweepTracker

def test_sweep_comparison():
    tracker = SweepTracker()
    # Schwab (0.45%) vs HYSA (4.5%)
    res = tracker.compare_rates("SCHWAB", 0.045)
    assert res["opportunity_cost_bps"] == 405.0
    assert res["recommendation"] == "SWEEP_TO_HYSA"

def test_stay_in_sweep():
    tracker = SweepTracker()
    # Vanguard (4.7%) vs HYSA (5.0%)
    res = tracker.compare_rates("VANGUARD", 0.05)
    # Spread is 0.3%, less than 1% threshold
    assert res["recommendation"] == "STAY"
