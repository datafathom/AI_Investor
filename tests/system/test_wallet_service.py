
import pytest
from services.crypto.wallet_service import WalletService
from unittest.mock import patch, MagicMock

@pytest.fixture
def service():
    # Force simulation mode for tests
    WalletService._instance = None
    return WalletService()

def test_wallet_balances_simulated(service):
    # Ensure service stays in simulation for this test
    service._is_simulated = True
    wallets = [{"address": "0x123", "chain": "eth"}, {"address": "abc", "chain": "sol"}]
    results = service.get_wallet_balances(wallets)
    assert len(results) == 2
    assert results[0]['symbol'] == 'ETH'

def test_verify_ownership_simulated(service):
    # Ensure service stays in simulation
    service._is_simulated = True
    result = service.verify_ownership("0x123", "sig", "msg")
    assert result is True

@patch('web3.Web3')
def test_eth_balance_call(mock_w3_class, service):
    # Set up mock w3 instance
    mock_w3 = MagicMock()
    mock_w3.eth.get_balance.return_value = 10**18 # 1 ETH
    mock_w3.from_wei.return_value = 1.0
    
    service._is_simulated = False
    service._w3 = mock_w3
    
    wallets = [{"address": "0x123", "chain": "eth"}]
    results = service.get_wallet_balances(wallets)
    
    assert len(results) == 1
    assert results[0]['balance'] == 1.0

