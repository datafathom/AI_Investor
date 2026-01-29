import pytest
from services.tax.roth_income_validator import RothIncomeValidator

def test_roth_eligibility_single():
    validator = RothIncomeValidator()
    # Under limit
    res = validator.validate_eligibility(100000, "SINGLE")
    assert res["allowed"] == True
    assert res["type"] == "FULL"
    
    # Over limit
    res = validator.validate_eligibility(170000, "SINGLE")
    assert res["allowed"] == False
    assert res["suggest_backdoor"] == True

def test_roth_eligibility_married():
    validator = RothIncomeValidator()
    # Phase out
    res = validator.validate_eligibility(235000, "MARRIED_JOINT")
    assert res["allowed"] == True
    assert res["type"] == "PARTIAL"
