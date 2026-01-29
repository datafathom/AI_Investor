import pytest
from decimal import Decimal
from uuid import UUID
from services.estate.dynasty_payout import DynastyPayoutEngine

@pytest.fixture
def payout_engine():
    return DynastyPayoutEngine()

def test_payout_engine_singleton():
    pe1 = DynastyPayoutEngine()
    pe2 = DynastyPayoutEngine()
    assert pe1 is pe2

def test_calculate_allowable_distribution_hems(payout_engine):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    beneficiary_id = UUID('87654321-4321-8765-4321-876543210987')
    
    # Valid HEMS purpose
    result = payout_engine.calculate_allowable_distribution(trust_id, Decimal('5000'), 'HEALTH', beneficiary_id)
    assert result['is_allowed'] is True
    assert result['approved_amount'] == Decimal('5000')
    
    # Invalid purpose
    result = payout_engine.calculate_allowable_distribution(trust_id, Decimal('5000'), 'LAMBORGHINI', beneficiary_id)
    assert result['is_allowed'] is False
    assert result['approved_amount'] == Decimal('0')
