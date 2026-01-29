import pytest
from services.real_estate.exchange_validator import ExchangeValidator1031

@pytest.fixture
def validator():
    return ExchangeValidator1031()

def test_exchange_validator_perfect_swap(validator):
    # $1M -> $1.2M swap (Greater value/equity)
    result = validator.validate_trade_up(1000000, 1200000, 500000, 600000)
    assert result['is_fully_tax_deferred'] is True
    assert result['estimated_boot'] == 0

def test_exchange_validator_boot(validator):
    # Relinquished $1M, Replacement $800k (Boot detected)
    result = validator.validate_trade_up(1000000, 800000, 500000, 400000)
    assert result['is_fully_tax_deferred'] is False
    assert result['estimated_boot'] > 0
