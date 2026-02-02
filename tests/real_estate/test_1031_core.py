import pytest
from decimal import Decimal
from services.real_estate.exchange_validator import ExchangeValidator

@pytest.fixture
def validator():
    return ExchangeValidator()

def test_exchange_validator_perfect_swap(validator):
    # $1M -> $1.2M swap (Greater value/equity)
    # Relinq: Val=1M, Eq=500k, Mtg=500k
    # Rep: Val=1.2M, Eq=600k, Mtg=600k
    result = validator.validate_metrics(
        Decimal('1000000'), Decimal('500000'), Decimal('500000'),
        Decimal('1200000'), Decimal('600000'), Decimal('600000')
    )
    assert result['is_fully_deferred'] is True
    assert result['taxable_boot_amount'] == 0

def test_exchange_validator_boot(validator):
    # Relinquished $1M, Replacement $800k (Boot detected)
    # Relinq: Val=1M, Eq=500k, Mtg=500k
    # Rep: Val=800k, Eq=400k, Mtg=400k
    result = validator.validate_metrics(
        Decimal('1000000'), Decimal('500000'), Decimal('500000'),
        Decimal('800000'), Decimal('400000'), Decimal('400000')
    )
    assert result['is_fully_deferred'] is False
    assert result['taxable_boot_amount'] > 0
