import pytest
from services.banking.banking_service import get_banking_service

def test_banking_service_singleton():
    s1 = get_banking_service()
    s2 = get_banking_service()
    assert s1 is s2

def test_create_link_token_simulated():
    service = get_banking_service()
    # Ensure it's in simulation mode for tests if no keys present
    service.is_simulated = True 
    token = service.create_link_token("user_123")
    assert token == "sim_link_token_12345"

def test_token_exchange_simulated():
    service = get_banking_service()
    service.is_simulated = True
    access_token = service.exchange_public_token("public_123")
    assert access_token == "sim_access_token_67890"

def test_get_accounts_simulated():
    service = get_banking_service()
    service.is_simulated = True
    accounts = service.get_accounts("access_123")
    assert len(accounts) == 3
    assert accounts[0]["name"] == "Main Checking"
    assert accounts[0]["balance"] == 15420.50
