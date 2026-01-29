import pytest
from services.compliance.competence_validator import CompetenceValidator

def test_competence_pass():
    validator = CompetenceValidator()
    res = validator.validate_competence("WEALTH_MANAGER", ["CFP", "SERIES_65", "CPA"])
    assert res["is_competent"] == True

def test_competence_fail():
    validator = CompetenceValidator()
    # Wealth Manager requires SERIES_65
    res = validator.validate_competence("WEALTH_MANAGER", ["CFP"])
    assert res["is_competent"] == False
    assert "SERIES_65" in res["missing_credentials"]
