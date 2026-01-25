"""
Tests for Enterprise API Endpoints
Phase 24: Enterprise Features & Multi-User Management
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.enterprise_api import enterprise_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(enterprise_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_enterprise_service():
    """Mock EnterpriseService."""
    with patch('web.api.enterprise_api.get_enterprise_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_multi_user_service():
    """Mock MultiUserService."""
    with patch('web.api.enterprise_api.get_multi_user_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_organization_success(client, mock_enterprise_service):
    """Test successful organization creation."""
    from models.enterprise import Organization
    
    mock_org = Organization(
        organization_id='org_1',
        name='Test Organization',
        parent_organization_id=None
    )
    mock_enterprise_service.create_organization.return_value = mock_org
    
    response = client.post('/api/enterprise/organization/create',
                          json={'name': 'Test Organization'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == 'Test Organization'


@pytest.mark.asyncio
async def test_create_organization_missing_name(client):
    """Test organization creation without name."""
    response = client.post('/api/enterprise/organization/create', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_create_team_success(client, mock_enterprise_service):
    """Test successful team creation."""
    from models.enterprise import Team
    
    mock_team = Team(
        team_id='team_1',
        organization_id='org_1',
        team_name='Test Team',
        members=[]
    )
    mock_enterprise_service.create_team.return_value = mock_team
    
    response = client.post('/api/enterprise/team/create',
                          json={
                              'organization_id': 'org_1',
                              'team_name': 'Test Team'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_share_resource_success(client, mock_multi_user_service):
    """Test successful resource sharing."""
    response = client.post('/api/enterprise/resource/share',
                          json={
                              'resource_id': 'resource_1',
                              'resource_type': 'portfolio',
                              'shared_with': ['user_2']
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
