"""
Tests for Institutional API Endpoints
Phase 26: Institutional Tools & Professional Features
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.institutional_api import institutional_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(institutional_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_institutional_service():
    """Mock InstitutionalService."""
    with patch('web.api.institutional_api.get_institutional_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_professional_tools_service():
    """Mock ProfessionalToolsService."""
    with patch('web.api.institutional_api.get_professional_tools_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_client_success(client, mock_institutional_service):
    """Test successful client creation."""
    from models.institutional import Client
    
    mock_client = Client(
        client_id='client_1',
        advisor_id='advisor_1',
        client_name='Test Client',
        portfolio_ids=[],
        created_date=None,
        updated_date=None
    )
    mock_institutional_service.create_client.return_value = mock_client
    
    response = client.post('/api/institutional/client/create',
                          json={
                              'advisor_id': 'advisor_1',
                              'client_name': 'Test Client'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['client_name'] == 'Test Client'


@pytest.mark.asyncio
async def test_create_client_missing_params(client):
    """Test client creation with missing parameters."""
    response = client.post('/api/institutional/client/create',
                          json={'advisor_id': 'advisor_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_configure_white_label_success(client, mock_institutional_service):
    """Test successful white-label configuration."""
    from models.institutional import WhiteLabelConfig
    
    mock_config = WhiteLabelConfig(
        organization_id='org_1',
        logo_url='https://example.com/logo.png',
        primary_color='#000000',
        secondary_color='#FFFFFF'
    )
    mock_institutional_service.configure_white_label.return_value = mock_config
    
    response = client.post('/api/institutional/whitelabel/configure',
                          json={
                              'organization_id': 'org_1',
                              'logo_url': 'https://example.com/logo.png',
                              'primary_color': '#000000'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
