"""
Tests for Enterprise API Endpoints
Phase 24: Enterprise Features & Multi-User Management
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.enterprise_api import router, get_enterprise_provider, get_multi_user_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "admin"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_enterprise_service(api_app):
    """Mock EnterpriseService."""
    service = AsyncMock()
    api_app.dependency_overrides[get_enterprise_provider] = lambda: service
    return service


@pytest.fixture
def mock_multi_user_service(api_app):
    """Mock MultiUserService."""
    service = AsyncMock()
    api_app.dependency_overrides[get_multi_user_provider] = lambda: service
    return service


def test_create_organization_success(client, mock_enterprise_service):
    """Test successful organization creation."""
    from schemas.enterprise import Organization
    
    mock_org = MagicMock()
    mock_org.model_dump.return_value = {
        'organization_id': 'org_1',
        'name': 'Test Organization',
        'parent_organization_id': None
    }
    mock_enterprise_service.create_organization.return_value = mock_org
    
    response = client.post('/api/v1/enterprise/organization/create',
                          json={'name': 'Test Organization'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['name'] == 'Test Organization'


def test_create_organization_missing_name(client):
    """Test organization creation without name."""
    response = client.post('/api/v1/enterprise/organization/create', json={})
    
    # Pydantic validation error returns 422
    assert response.status_code == 422


def test_create_team_success(client, mock_enterprise_service):
    """Test successful team creation."""
    mock_team = MagicMock()
    mock_team.model_dump.return_value = {
        'team_id': 'team_1',
        'organization_id': 'org_1',
        'team_name': 'Test Team',
        'members': []
    }
    mock_enterprise_service.create_team.return_value = mock_team
    
    response = client.post('/api/v1/enterprise/team/create',
                          json={
                              'organization_id': 'org_1',
                              'team_name': 'Test Team'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_share_resource_success(client, mock_multi_user_service):
    """Test successful resource sharing."""
    mock_resource = MagicMock()
    mock_resource.model_dump.return_value = {
        'resource_id': 'resource_1',
        'resource_type': 'portfolio',
        'team_id': 'team_1',
        'permissions': {}
    }
    mock_multi_user_service.share_resource.return_value = mock_resource
    
    response = client.post('/api/v1/enterprise/resource/share',
                          json={
                              'resource_id': 'resource_1',
                              'resource_type': 'portfolio',
                              'team_id': 'team_1'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
