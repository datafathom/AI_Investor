import pytest
from services.compliance.ppli_gate import PPLIEligibilityGate

def test_ppli_eligible_nw():
    svc = PPLIEligibilityGate()
    # 15M NW -> Eligible
    res = svc.check_eligibility(15000000, 1000000)
    assert res["is_eligible"] == True

def test_ppli_eligible_inv():
    svc = PPLIEligibilityGate()
    # 8M Inv -> Eligible
    res = svc.check_eligibility(2000000, 8000000)
    assert res["is_eligible"] == True

def test_ppli_ineligible():
    svc = PPLIEligibilityGate()
    # 2M NW, 1M Inv -> Ineligible
    res = svc.check_eligibility(2000000, 1000000)
    assert res["is_eligible"] == False
