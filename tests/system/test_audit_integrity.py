
import pytest
from unittest.mock import MagicMock, patch
from services.system.audit_integrity_service import AuditIntegrityService
from services.system.activity_service import ActivityService

@pytest.fixture
def audit_service():
    return AuditIntegrityService()

def test_calculate_hash(audit_service):
    data = {"key": "value"}
    prev = "hash1"
    h1 = audit_service.calculate_hash(data, prev)
    h2 = audit_service.calculate_hash(data, prev)
    assert h1 == h2
    assert isinstance(h1, str)
    assert len(h1) == 64 # sha256 hex length

@pytest.fixture
def activity_service():
    ActivityService._instance = None
    with patch('services.system.activity_service.get_database_manager') as mock_db:
        service = ActivityService()
        service.db = MagicMock()
        return service

def test_log_activity_flow(activity_service):
    # Mock DB Interactions
    mock_cursor = MagicMock()
    activity_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    # Mock "get previous hash"
    mock_cursor.fetchone.side_effect = [
        ("PREV_HASH",),          # select prev hash
        ("new-uuid", "2023-01-01") # insert returning
    ]
    
    activity_service.log_activity("user-1", "LOGIN", {"ip": "1.1.1.1"})
    
    # Check calls
    assert mock_cursor.execute.call_count == 3 # Select Prev, Insert, Update Hash
    
    # Verify Insert args
    insert_call = mock_cursor.execute.call_args_list[1]
    assert "INSERT INTO activity_logs" in insert_call[0][0]
    assert "user-1" in insert_call[0][1]
    
    # Verify Update args includes a hash
    update_call = mock_cursor.execute.call_args_list[2]
    assert "UPDATE activity_logs" in update_call[0][0]
    # Check that update has a string argument for hash
    assert isinstance(update_call[0][1][0], str)
