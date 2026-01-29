import pytest
from services.performance.recovery_tracker import RecoveryTracker
from datetime import date, timedelta

def test_recovery_active_drawdown():
    svc = RecoveryTracker()
    # Peak 100k, now 90k
    res = svc.analyze_recovery(90000, 100000, date.today() - timedelta(days=10))
    assert res["is_under_peak"] == True
    assert res["drawdown_pct"] == 0.1
    assert res["days_since_peak"] == 10

def test_full_recovery():
    svc = RecoveryTracker()
    # At new peak
    res = svc.analyze_recovery(110000, 100000, date.today() - timedelta(days=20))
    assert res["is_under_peak"] == False
    assert res["drawdown_pct"] == 0.0
