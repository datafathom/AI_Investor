import pytest
from uuid import UUID
from decimal import Decimal
from services.compliance.clawback_preventer import ClawbackPreventer

@pytest.fixture
def preventer():
    return ClawbackPreventer()

def test_clawback_preventer_singleton():
    s1 = ClawbackPreventer()
    s2 = ClawbackPreventer()
    assert s1 is s2

def test_validate_withdrawal_revocable(preventer):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    person_id = UUID('87654321-4321-8765-4321-876543210987')
    # Allowed in revocable even if to grantor
    result = preventer.validate_withdrawal(trust_id, 'REVOCABLE', Decimal('1000'), person_id, person_id)
    assert result['is_valid'] is True

def test_validate_withdrawal_irrevocable_clawback(preventer):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    person_id = UUID('87654321-4321-8765-4321-876543210987')
    # Blocked in irrevocable if to grantor
    result = preventer.validate_withdrawal(trust_id, 'IRREVOCABLE', Decimal('1000'), person_id, person_id)
    assert result['is_valid'] is False
    assert result['reason'] == "ILLEGAL_CLAWBACK_IN_IRREVOCABLE_TRUST"
