import pytest
from uuid import UUID
from services.compliance.blind_redactor import BlindTrustRedactor
from services.trading.beneficiary_blocker import BeneficiaryOrderBlocker

@pytest.fixture
def redactor():
    return BlindTrustRedactor()

@pytest.fixture
def blocker():
    return BeneficiaryOrderBlocker()

def test_blind_redactor_active(redactor):
    data = {
        "total_market_value": 1000000,
        "holdings": [{"symbol": "AAPL", "value": 500000}, {"symbol": "TSLA", "value": 500000}]
    }
    result = redactor.redact_portfolio_data(data, "BLIND_BENEFICIARY")
    assert result['is_redacted'] is True
    assert result['holdings'][0]['symbol'] == "HIDDEN"

def test_beneficiary_blocker_violation(blocker):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    user_id = UUID('87654321-4321-8765-4321-876543210987')
    # Beneficiary cannot trade
    result = blocker.validate_order_source(user_id, "BLIND_BENEFICIARY", trust_id)
    assert result['is_order_accepted'] is False
    assert result['reason'] == "FIDUCIARY_CONTROL_REQUIRED"
