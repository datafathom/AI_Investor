"""
Tests for Gmail API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.gmail_api import router


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_send_email_missing_token(client):
    """Test email sending without access token."""
    response = client.post('/api/v1/gmail/send',
                          json={
                              'to': 'user@example.com',
                              'subject': 'Test',
                              'body_text': 'Hello'
                          })
    
    # Returns 401 for missing token
    assert response.status_code == 401


def test_preview_template_success(client):
    """Test successful template preview."""
    with patch('services.communication.email_templates.get_email_template_engine') as mock_engine:
        engine = MagicMock()
        engine.render_template.return_value = ("Plain text", "<html>HTML</html>")
        mock_engine.return_value = engine
        
        response = client.get('/api/v1/gmail/preview?template_name=test_template')
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['template_name'] == 'test_template'


def test_get_stats_success(client):
    """Test successful stats retrieval."""
    with patch('services.communication.gmail_service.get_gmail_service') as mock_service:
        service = AsyncMock()
        service.get_send_statistics.return_value = {'emails_sent': 10, 'emails_failed': 1}
        mock_service.return_value = service
        
        response = client.get('/api/v1/gmail/stats')
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
