
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.briefing_api import router, get_briefing_gen
from web.auth_utils import get_current_user

@pytest.fixture
def api_app(mock_briefing_generator):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_briefing_gen] = lambda: mock_briefing_generator
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_briefing_generator():
    """Mock BriefingGenerator."""
    generator = AsyncMock()
    return generator

def test_get_daily_briefing_success(client, mock_briefing_generator):
    """Test successful daily briefing retrieval."""
    mock_result = {'briefing': 'Good morning, Commander. Your portfolio is performing well.'}
    mock_briefing_generator.get_daily_briefing.return_value = mock_result
    
    response = client.get('/api/v1/ai/briefing/daily?mock=true')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['briefing'] == 'Good morning, Commander. Your portfolio is performing well.'
