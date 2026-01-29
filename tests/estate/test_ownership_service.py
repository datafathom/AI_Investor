import pytest
from uuid import UUID
from services.estate.ownership_service import OwnershipService

@pytest.fixture
def ownership_service():
    return OwnershipService()

def test_ownership_service_singleton():
    os1 = OwnershipService()
    os2 = OwnershipService()
    assert os1 is os2

def test_link_trust_to_portfolio(ownership_service):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    portfolio_id = UUID('11111111-2222-3333-4444-555555555555')
    result = ownership_service.link_trust_to_portfolio(trust_id, portfolio_id, 'VERIFIED')
    assert result is True

def test_verify_titling(ownership_service):
    asset_id = UUID('11111111-2222-3333-4444-555555555555')
    result = ownership_service.verify_titling(asset_id)
    assert result == "VERIFIED"
