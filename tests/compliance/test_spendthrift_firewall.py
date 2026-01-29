import pytest
from uuid import UUID
from decimal import Decimal
from services.compliance.spendthrift_firewall import SpendthriftFirewall

@pytest.fixture
def firewall():
    return SpendthriftFirewall()

def test_spendthrift_firewall_singleton():
    s1 = SpendthriftFirewall()
    s2 = SpendthriftFirewall()
    assert s1 is s2

def test_validate_distribution_creditor(firewall):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    creditor_id = UUID('11111111-2222-3333-4444-555555555555')
    # Blocked for creditor
    result = firewall.validate_distribution_request(trust_id, Decimal('10000'), creditor_id, 'CREDITOR')
    assert result['is_allowed'] is False
    assert result['reason'] == "SPENDTHRIFT_PROTECTION_ACTIVE"

def test_validate_distribution_beneficiary(firewall):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    beneficiary_id = UUID('87654321-4321-8765-4321-876543210987')
    # Allowed for beneficiary
    result = firewall.validate_distribution_request(trust_id, Decimal('10000'), beneficiary_id, 'BENEFICIARY')
    assert result['is_allowed'] is True
