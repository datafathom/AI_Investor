"""
Tests for Estate Planning API Endpoints
Phase 9: Estate Planning & Inheritance Simulation
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.estate_api import estate_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(estate_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_estate_planning_service():
    """Mock EstatePlanningService."""
    with patch('web.api.estate_api.get_estate_planning_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_inheritance_simulator():
    """Mock InheritanceSimulator."""
    with patch('web.api.estate_api.get_inheritance_simulator') as mock:
        simulator = AsyncMock()
        mock.return_value = simulator
        yield simulator


@pytest.mark.asyncio
async def test_create_estate_plan_success(client, mock_estate_planning_service):
    """Test successful estate plan creation."""
    from models.estate import EstatePlan
    
    mock_plan = EstatePlan(
        plan_id='plan_1',
        user_id='user_1',
        beneficiaries=[],
        total_estate_value=1000000.0
    )
    mock_estate_planning_service.create_estate_plan.return_value = mock_plan
    
    response = client.post('/api/estate/plan/create',
                          json={
                              'user_id': 'user_1',
                              'beneficiaries': []
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_create_estate_plan_missing_params(client):
    """Test estate plan creation with missing parameters."""
    response = client.post('/api/estate/plan/create', json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_estate_plan_success(client, mock_estate_planning_service):
    """Test successful estate plan retrieval."""
    from models.estate import EstatePlan
    
    mock_plan = EstatePlan(
        plan_id='plan_1',
        user_id='user_1',
        beneficiaries=[],
        total_estate_value=1000000.0
    )
    mock_estate_planning_service.get_estate_plan.return_value = mock_plan
    
    response = client.get('/api/estate/plan/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_calculate_estate_tax_success(client, mock_estate_planning_service):
    """Test successful estate tax calculation."""
    from models.estate import EstateTaxCalculation
    
    mock_calculation = EstateTaxCalculation(
        plan_id='plan_1',
        total_estate_value=1000000.0,
        taxable_amount=500000.0,
        estimated_tax=200000.0
    )
    mock_estate_planning_service.calculate_estate_tax.return_value = mock_calculation
    
    response = client.post('/api/estate/tax/calculate',
                          json={'plan_id': 'plan_1'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
