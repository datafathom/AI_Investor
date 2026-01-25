
import pytest
from unittest.mock import MagicMock, patch
from services.system.health_check_service import HealthCheckService

@pytest.fixture
def health_check_service():
    HealthCheckService._instance = None
    with patch('services.system.health_check_service.get_database_manager') as mock_db, \
         patch('services.system.health_check_service.get_cache_service') as mock_cache:
        service = HealthCheckService()
        service.db = MagicMock()
        service.cache = MagicMock()
        return service

def test_health_check_postgres_up(health_check_service):
    # Mock successful query
    mock_cursor = MagicMock()
    health_check_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    
    res = health_check_service.check_postgres()
    assert res['status'] == 'UP'
    assert 'latency_ms' in res

def test_health_check_postgres_down(health_check_service):
    # Mock failure
    health_check_service.db.pg_cursor.side_effect = Exception("Connection Refused")
    
    res = health_check_service.check_postgres()
    assert res['status'] == 'DOWN'
    assert res['error'] == "Connection Refused"

def test_full_status_aggregation(health_check_service):
    # Mock both UP
    mock_cursor = MagicMock()
    health_check_service.db.pg_cursor.return_value.__enter__.return_value = mock_cursor
    health_check_service.cache.get.return_value = True
    
    status = health_check_service.get_full_status()
    assert status['overall'] == 'UP'
    assert status['postgres']['status'] == 'UP'
    assert status['redis']['status'] == 'UP'
