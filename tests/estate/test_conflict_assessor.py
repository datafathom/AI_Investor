import pytest
from services.estate.conflict_assessor import ConflictAssessor

@pytest.fixture
def assessor():
    return ConflictAssessor()

def test_calculate_litigation_risk_critical(assessor):
    # Step kids + Unequal + House = 25+20+15 = 60 (Critical)
    result = assessor.calculate_litigation_risk(True, True, True)
    assert result['risk_score'] == 60
    assert result['risk_level'] == "HIGH"
    assert any("In Terrorem" in r for r in result['recommendations'])

def test_calculate_litigation_risk_low(assessor):
    # Simple family, fair split
    result = assessor.calculate_litigation_risk(False, False, False)
    assert result['risk_score'] == 0
    assert result['risk_level'] == "LOW"
