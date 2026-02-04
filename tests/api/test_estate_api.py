"""
Tests for Estate Planning API Endpoints
Phase 9: Estate Planning & Inheritance Simulation
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from web.api.estate_api import router, get_estate_planning_provider, get_inheritance_simulator_provider


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


@pytest.fixture
def mock_estate_planning_service(api_app):
    """Mock EstatePlanningService."""
    service = AsyncMock()
    api_app.dependency_overrides[get_estate_planning_provider] = lambda: service
    return service


@pytest.fixture
def mock_inheritance_simulator(api_app):
    """Mock InheritanceSimulator."""
    simulator = AsyncMock()
    api_app.dependency_overrides[get_inheritance_simulator_provider] = lambda: simulator
    return simulator


def test_create_estate_plan_success(client, mock_estate_planning_service):
    """Test successful estate plan creation."""
    mock_plan = MagicMock()
    mock_plan.model_dump.return_value = {
        'plan_id': 'plan_1',
        'user_id': 'user_1',
        'total_estate_value': 1000000.0,
        'beneficiaries': [],
        'created_date': datetime.now(timezone.utc).isoformat(),
        'updated_date': datetime.now(timezone.utc).isoformat()
    }
    mock_estate_planning_service.create_estate_plan.return_value = mock_plan
    
    beneficiary = {
        'name': 'John Doe',
        'relationship': 'child',
        'allocation_percentage': 50.0
    }
    
    response = client.post('/api/v1/estate/plan/create',
                          json={
                              'user_id': 'user_1',
                              'beneficiaries': [beneficiary]
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_create_estate_plan_missing_params(client):
    """Test estate plan creation with missing parameters."""
    response = client.post('/api/v1/estate/plan/create', json={'user_id': 'user_1'})
    
    # Pydantic validation error returns 422
    assert response.status_code == 422


def test_get_estate_plan_success(client, mock_estate_planning_service):
    """Test successful estate plan retrieval."""
    mock_plan = MagicMock()
    mock_plan.model_dump.return_value = {
        'plan_id': 'plan_1',
        'user_id': 'user_1',
        'total_estate_value': 1000000.0,
        'beneficiaries': [],
        'created_date': datetime.now(timezone.utc).isoformat(),
        'updated_date': datetime.now(timezone.utc).isoformat()
    }
    mock_estate_planning_service.get_estate_plan_by_user.return_value = mock_plan
    
    response = client.get('/api/v1/estate/plan/user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True


def test_calculate_estate_tax_success(client, mock_estate_planning_service):
    """Test successful estate tax calculation."""
    mock_calculation = {
        'estate_value': 1000000.0,
        'exemption': 12000000.0,
        'taxable_estate': 0.0,
        'estate_tax': 0.0
    }
    mock_estate_planning_service.calculate_estate_tax.return_value = mock_calculation
    
    response = client.post('/api/v1/estate/tax/calculate',
                          json={'estate_value': 1000000.0})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
