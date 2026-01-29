import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from flask import Flask
from web.api.institutional_api import institutional_bp
from models.institutional import Client, WhiteLabelConfig

from datetime import datetime

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    # We patch login_required to be a no-op decorator for tests
    # Note: We must patch it in the module where it's USED
    with patch('web.api.institutional_api.login_required', lambda x: x):
        app.register_blueprint(institutional_bp)
    return app

@pytest.fixture
def client(app):
    """Test client fixture."""
    return app.test_client()

@pytest.fixture
def mock_service():
    """Mock InstitutionalService fixture."""
    with patch('web.api.institutional_api.get_institutional_service') as mock:
        service = MagicMock() # Use MagicMock for sync access to AsyncMock return values if needed
        mock.return_value = service
        yield service

def test_create_client_success(client, mock_service):
    """Test successful client creation via API."""
    now = datetime.utcnow()
    mock_service.create_client = AsyncMock(return_value=Client(
        client_id='client_123',
        advisor_id='advisor_1',
        client_name='Test Client',
        portfolio_ids=[],
        created_date=now,
        updated_date=now
    ))
    
    response = client.post('/api/v1/institutional/client/create',
                          json={
                              'advisor_id': 'advisor_1',
                              'client_name': 'Test Client'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['client_name'] == 'Test Client'

def test_get_fee_analytics(client, mock_service):
    """Test fee analytics endpoint."""
    mock_service.get_revenue_forecast = AsyncMock(return_value={
        'current_fees': 1250000.0,
        'projected_fees': 1306250.0,
        'growth_rate': 0.045
    })
    
    response = client.get('/api/v1/institutional/analytics/fees')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['current_fees'] == 1250000.0

def test_get_risk_analytics(client, mock_service):
    """Test risk analytics endpoint."""
    mock_service.get_client_risk_profile = AsyncMock(return_value={
        'volatility_score': 15.5,
        'health_status': 'Healthy'
    })
    
    response = client.get('/api/v1/institutional/analytics/risk/client_123')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['volatility_score'] == 15.5

def test_get_signatures(client, mock_service):
    """Test document signatures endpoint."""
    mock_service.get_signature_status = AsyncMock(return_value={
        'completion_percentage': 75.0,
        'is_fully_signed': False
    })
    
    response = client.get('/api/v1/institutional/analytics/signatures/client_123')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['completion_percentage'] == 75.0

def test_get_allocation(client, mock_service):
    """Test asset allocation endpoint."""
    mock_service.get_asset_allocation = AsyncMock(return_value={
        'total_aum': 120000000.0,
        'allocations': []
    })
    
    response = client.get('/api/v1/institutional/analytics/allocation/client_123')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['total_aum'] == 120000000.0

def test_configure_white_label(client, mock_service):
    """Test white-label configuration."""
    now = datetime.utcnow()
    mock_service.configure_white_label = AsyncMock(return_value=WhiteLabelConfig(
        config_id='cfg_123',
        organization_id='org_1',
        branding_name='Test Brand',
        created_date=now,
        updated_date=now
    ))
    
    response = client.post('/api/v1/institutional/whitelabel/configure',
                          json={'organization_id': 'org_1', 'branding_name': 'Test Brand'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['branding_name'] == 'Test Brand'
