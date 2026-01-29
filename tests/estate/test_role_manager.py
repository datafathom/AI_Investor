import pytest
from uuid import UUID
from services.estate.role_manager import RoleManager

@pytest.fixture
def role_manager():
    return RoleManager()

def test_role_manager_singleton():
    rm1 = RoleManager()
    rm2 = RoleManager()
    assert rm1 is rm2

def test_assign_role(role_manager):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    person_id = UUID('87654321-4321-8765-4321-876543210987')
    result = role_manager.assign_role(trust_id, person_id, 'TRUSTEE', {'type': 'PRIMARY'})
    assert result is True

def test_validate_role_permissions(role_manager):
    trust_id = UUID('12345678-1234-5678-1234-567812345678')
    person_id = UUID('87654321-4321-8765-4321-876543210987')
    result = role_manager.validate_role_permissions(person_id, trust_id, 'WITHDRAW')
    assert result is True
