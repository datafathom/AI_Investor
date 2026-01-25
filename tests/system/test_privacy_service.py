
import pytest
from unittest.mock import MagicMock, patch
from services.system.privacy_service import PrivacyService

@pytest.fixture
def privacy_service():
    """Fixture to provide a PrivacyService with a mocked database manager."""
    PrivacyService._instance = None
    with patch('services.system.privacy_service.get_database_manager') as mock_db_getter:
        # Patch the db attribute directly on the instance
        service = PrivacyService()
        service.db = MagicMock()
        return service

def test_export_data(privacy_service):
    # Mock PG cursor and data
    mock_cursor = MagicMock()
    privacy_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    # Mocking user profile result
    mock_cursor.fetchone.return_value = ('test@example.com', 'testuser', None, 'user')
    # Mocking activity and portfolio
    mock_cursor.fetchall.side_effect = [[], []] 

    data = privacy_service.export_user_data('user-123')
    
    assert data['metadata']['user_id'] == 'user-123'
    assert data['user_profile']['email'] == 'test@example.com'
    assert mock_cursor.execute.called

def test_delete_account(privacy_service):
    # Mock PG deletion
    mock_cursor = MagicMock()
    privacy_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    success = privacy_service.delete_user_account('user-123')
    
    assert success is True
    assert privacy_service.db.run_neo4j_query.called
    assert mock_cursor.execute.called
