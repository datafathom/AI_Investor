import pytest
from services.estate.allowance_engine import AllowanceEngine

def test_allowance_approved_under_limit():
    svc = AllowanceEngine()
    # 5k limit, 2k already spent, request 1k -> Approved
    res = svc.validate_withdrawal(1000, 5000, 2000)
    assert res["is_approved"] == True
    assert res["remaining_budget"] == 2000.0

def test_allowance_blocked_over_limit():
    svc = AllowanceEngine()
    # 5k limit, 4k already spent, request 2k -> Blocked
    res = svc.validate_withdrawal(2000, 5000, 4000)
    assert res["is_approved"] == False
    assert res["approved_amount"] == 0.0

def test_allowance_emergency_bypass():
    svc = AllowanceEngine()
    # Over limit but emergency -> Approved
    res = svc.validate_withdrawal(10000, 5000, 0, is_emergency=True)
    assert res["is_approved"] == True
