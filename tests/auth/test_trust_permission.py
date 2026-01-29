import pytest
from uuid import UUID
from services.auth.trust_permission import TrustPermissionService

@pytest.fixture
def permission_service():
    return TrustPermissionService()

def test_trust_permission_singleton():
    s1 = TrustPermissionService()
    s2 = TrustPermissionService()
    assert s1 is s2

def test_check_permission_revocable(permission_service):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    user_id = UUID('87654321-4321-8765-4321-876543210987')
    # All actions allowed for revocable
    assert permission_service.check_permission(trust_id, 'REVOCABLE', 'WITHDRAW', user_id) is True
    assert permission_service.check_permission(trust_id, 'REVOCABLE', 'AMEND', user_id) is True

def test_check_permission_irrevocable(permission_service):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    user_id = UUID('87654321-4321-8765-4321-876543210987')
    # Selective actions for irrevocable
    assert permission_service.check_permission(trust_id, 'IRREVOCABLE', 'WITHDRAW', user_id) is False
    assert permission_service.check_permission(trust_id, 'IRREVOCABLE', 'INVEST', user_id) is True
