import pytest
from services.tax.roth_contribution_validator import RothContributionValidator

def test_roth_allowed():
    svc = RothContributionValidator()
    # 100k -> Allowed
    res = svc.validate_direct_contribution(100000)
    assert res["status"] == "ALLOWED"

def test_roth_blocked_for_high_income():
    svc = RothContributionValidator()
    # 200k -> Blocked
    res = svc.validate_direct_contribution(200000)
    assert res["status"] == "BLOCKED"
    assert res["suggestion"] == "BACKDOOR_ROTH"
