import pytest
from services.compliance.leverage_blocker import LeverageBlocker

def test_pledge_blocked_irrevocable():
    svc = LeverageBlocker()
    res = svc.can_pledge_as_collateral("IRREVOCABLE", False)
    assert res["can_pledge"] == False
    assert res["shield_status"] == "ACTIVE"

def test_pledge_blocked_spendthrift():
    svc = LeverageBlocker()
    # Revocable but spendthrift -> Blocked
    res = svc.can_pledge_as_collateral("REVOCABLE", True)
    assert res["can_pledge"] == False

def test_pledge_allowed_standard_rlt():
    svc = LeverageBlocker()
    # Revocable, not spendthrift -> Allowed
    res = svc.can_pledge_as_collateral("REVOCABLE", False)
    assert res["can_pledge"] == True
