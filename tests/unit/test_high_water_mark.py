import pytest
from services.billing.high_water_mark import HWMTracker

def test_performance_fee_triggered():
    tracker = HWMTracker()
    # High Water Mark 1M, Current NAV 1.2M, Carry 20%
    # Gain 200k @ 20% = 40,000
    fee = tracker.calculate_incentive_fee(1200000, 1000000, 0.20)
    assert fee == 40000.0

def test_performance_fee_blocked():
    tracker = HWMTracker()
    # Below HWM -> No fee
    fee = tracker.calculate_incentive_fee(900000, 1000000, 0.20)
    assert fee == 0.0
