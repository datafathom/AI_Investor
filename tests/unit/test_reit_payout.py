import pytest
from services.reits.payout_validator import REITPayoutValidator

def test_payout_compliance():
    svc = REITPayoutValidator()
    # 10M income, 9.5M paid (95%) -> OK
    res = svc.validate_payout(10000000, 9500000)
    assert res["is_compliant"] == True

def test_payout_violation():
    svc = REITPayoutValidator()
    # 10M income, 8M paid (80%) -> FAIL (Needs 90%)
    res = svc.validate_payout(10000000, 8000000)
    assert res["is_compliant"] == False
    assert res["shortfall"] == 1000000.0
