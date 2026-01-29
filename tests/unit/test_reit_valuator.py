import pytest
from services.reits.split_share_valuator import SplitShareValuator

def test_yield_spread():
    svc = SplitShareValuator()
    # Pref 7%, Common 5%
    assert svc.calculate_yield_spread(0.07, 0.05) == 0.02

def test_risk_by_ltv():
    svc = SplitShareValuator()
    assert svc.assess_risk_profile(0.35) == "CONSERVATIVE"
    assert svc.assess_risk_profile(0.55) == "MODERATE"
    assert svc.assess_risk_profile(0.70) == "AGGRESSIVE"
