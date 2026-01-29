import pytest
from services.retirement.principal_gate import PrincipalGateService

def test_principal_tap_detection():
    svc = PrincipalGateService()
    # 1M start, now 900k (Underwater). Any withdrawal is a tap.
    res = svc.validate_withdrawal_intent(900000, 1000000, 5000)
    assert res["is_tapping_principal"] == True

def test_excess_growth_safe():
    svc = PrincipalGateService()
    # 1M start, now 1.2M. Can take 100k safely.
    res = svc.validate_withdrawal_intent(1200000, 1000000, 100000)
    assert res["is_tapping_principal"] == False
    assert res["excess_growth_available"] == 200000.0

def test_excess_growth_too_much():
    svc = PrincipalGateService()
    # 1.2M total, 200k growth. Tries to take 300k.
    res = svc.validate_withdrawal_intent(1200000, 1000000, 300000)
    assert res["is_tapping_principal"] == True
