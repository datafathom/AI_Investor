import pytest
from services.compliance.hems_validator import HEMSValidator

def test_hems_qualified_medical():
    svc = HEMSValidator()
    res = svc.validate_payout("SURGERY", 50000)
    assert res["is_hems_qualified"] == True
    assert res["category"] == "HEALTH"

def test_hems_qualified_education():
    svc = HEMSValidator()
    res = svc.validate_payout("TUITION", 15000)
    assert res["is_hems_qualified"] == True
    assert res["category"] == "EDUCATION"

def test_hems_discretionary_luxury():
    svc = HEMSValidator()
    # Buying a Yacht is not HEMS
    res = svc.validate_payout("YACHT_MAINTENANCE", 100000)
    assert res["is_hems_qualified"] == False
