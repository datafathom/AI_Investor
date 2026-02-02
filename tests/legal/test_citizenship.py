import pytest
from decimal import Decimal
from services.legal.citizenship_service import CitizenshipService
from services.legal.passport_gate import PassportGate

@pytest.fixture
def c_svc():
    return CitizenshipService()

@pytest.fixture
def gate():
    return PassportGate()

def test_get_program_details(c_svc):
    res = c_svc.get_program_details("PORTUGAL")
    assert res["cost"] == Decimal("500000.00")
    assert res["eu_access"] is True
    
    bad = c_svc.get_program_details("MARS")
    assert "error" in bad

def test_calculate_stateless_risk(c_svc):
    # No passport -> Critical
    res = c_svc.calculate_stateless_risk(False, 0.9)
    assert res["risk_score"] == 0.9
    assert res["is_critical"] is True
    
    # Stable home -> Low risk
    res2 = c_svc.calculate_stateless_risk(True, 0.9)
    assert res2["risk_score"] <= 0.1
    assert res2["is_critical"] is False

def test_verify_eu_access(gate):
    # US pass buying in FR -> Restricted
    res = gate.verify_eu_access(["US"], "FR")
    assert res["can_acquire"] is False
    
    # PT pass buying in FR -> Permitted
    res2 = gate.verify_eu_access(["PT"], "FR")
    assert res2["can_acquire"] is True
    
    # US pass buying in US -> Permitted (not EU asset)
    res3 = gate.verify_eu_access(["US"], "US")
    assert res3["can_acquire"] is True
