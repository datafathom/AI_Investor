import pytest
from services.market.active_passive_tracker import ActivePassiveTracker

def test_passive_dominance_breach():
    tracker = ActivePassiveTracker()
    # Active Vol 10k, Passive Flows 90k -> 90% passive
    res = tracker.calculate_passive_dominance("SPY", 10000, 90000)
    assert res["passive_pct"] == 0.9
    assert res["threshold_breach"] == True

def test_active_dominance():
    tracker = ActivePassiveTracker()
    # Active Vol 50k, Passive 10k -> 16.6% passive
    res = tracker.calculate_passive_dominance("AAPL", 50000, 10000)
    assert res["threshold_breach"] == False
