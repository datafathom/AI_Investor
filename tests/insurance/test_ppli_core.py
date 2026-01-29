import pytest
from uuid import UUID
from decimal import Decimal
from services.insurance.loan_tracker import PPLILoanTracker
from services.compliance.ppli_gate import PPLIEligibilityGate

@pytest.fixture
def loan_tracker():
    return PPLILoanTracker()

@pytest.fixture
def eligibility_gate():
    return PPLIEligibilityGate()

def test_calculate_lapse_risk(loan_tracker):
    # $1M value, $500k loan, $50k COI -> 10 years
    risk = loan_tracker.calculate_lapse_risk(Decimal('1000000'), Decimal('500000'), Decimal('50000'))
    assert risk == 10

def test_ppli_eligibility_qp(eligibility_gate):
    # $6M individual passes QP test
    result = eligibility_gate.check_eligibility("user_123", 6000000, "INDIVIDUAL")
    assert result['is_eligible'] is True
    assert result['accreditation_level'] == "QUALIFIED_PURCHASER"

def test_ppli_eligibility_retail(eligibility_gate):
    # $2M individual fails QP test
    result = eligibility_gate.check_eligibility("user_456", 2000000, "INDIVIDUAL")
    assert result['is_eligible'] is False
    assert result['accreditation_level'] == "RETAIL"
