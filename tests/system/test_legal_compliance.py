
import pytest
from unittest.mock import MagicMock, patch
from services.system.legal_compliance_service import LegalComplianceService

@pytest.fixture
def legal_service():
    LegalComplianceService._instance = None
    with patch('services.system.legal_compliance_service.get_database_manager') as mock_db:
        service = LegalComplianceService()
        service.db = MagicMock()
        return service

def test_get_user_consent_status(legal_service):
    # Mock DB response: User has accepted TOS v0.9 (Old)
    mock_cursor = MagicMock()
    legal_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    # user_consents table returns: type, version, date
    mock_cursor.fetchall.return_value = [
        ("TOS", "0.9", "2023-01-01")
    ]
    
    status = legal_service.get_user_consent_status("u1")
    
    assert status['tos']['version'] == "0.9"
    assert status['is_tos_current'] is False # v1.0 is required
    assert status['is_risk_current'] is False # Not accepted at all

def test_accept_agreement(legal_service):
    mock_cursor = MagicMock()
    legal_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    success = legal_service.accept_agreement("u1", "TOS", "1.0")
    
    assert success is True
    assert mock_cursor.execute.call_count == 1
    args = mock_cursor.execute.call_args[0]
    assert "INSERT INTO user_consents" in args[0]
    assert "1.0" in args[1] # Params
