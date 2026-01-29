import pytest
from uuid import UUID
from services.trusts.remainder_trigger import RemainderTrigger
from services.compliance.charity_verifier import CharityVerifier

@pytest.fixture
def trigger():
    return RemainderTrigger()

@pytest.fixture
def verifier():
    return CharityVerifier()

def test_evaluate_termination(trigger):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    # Termination date reached
    assert trigger.evaluate_termination(trust_id, '2026-01-26', '2026-01-26') is True
    # Not yet terminated
    assert trigger.evaluate_termination(trust_id, '2026-01-25', '2026-01-26') is False

def test_verify_charity_standing(verifier):
    result = verifier.verify_charity_standing("12-3456789", "Red Cross")
    assert result['is_valid_501c3'] is True
    assert result['status'] == "ELGIIBLE"
