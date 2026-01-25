
import pytest
from services.brokerage.settlement_service import SettlementService

@pytest.fixture
def service():
    SettlementService._instance = None
    return SettlementService()

def test_balance_summary(service):
    summary = service.get_balance_summary()
    assert summary['base_currency'] == 'USD'
    assert summary['total_equity_usd'] > 0
    assert len(summary['balances']) >= 4

def test_currency_conversion(service):
    # Initial EUR balance
    initial_eur = service._balances['EUR']
    
    # Sell 1000 USD for EUR
    result = service.convert_currency('USD', 'EUR', 1000.0)
    
    assert result['status'] == 'SUCCESS'
    assert result['amount_sold'] == 1000.0
    assert result['amount_bought'] > 0
    
    # Verify balances updated
    assert service._balances['USD'] == 49000.0
    assert service._balances['EUR'] > initial_eur

def test_insufficient_funds(service):
    result = service.convert_currency('GBP', 'USD', 1000000.0)
    assert result['status'] == 'ERROR'
    assert 'Insufficient funds' in result['message']

def test_unsupported_currency(service):
    result = service.convert_currency('BTC', 'USD', 1.0)
    assert result['status'] == 'ERROR'
    assert 'Unsupported currency' in result['message']
