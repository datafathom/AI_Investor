
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from web.api.dashboard_api import router, get_dynamic_allocator, get_risk_monitor, get_circuit_breaker, get_paper_exchange, login_required

@pytest.fixture
def api_app(mock_allocator, mock_risk_monitor, mock_circuit_breaker, mock_paper_exchange):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_dynamic_allocator] = lambda: mock_allocator
    app.dependency_overrides[get_risk_monitor] = lambda: mock_risk_monitor
    app.dependency_overrides[get_circuit_breaker] = lambda: mock_circuit_breaker
    app.dependency_overrides[get_paper_exchange] = lambda: mock_paper_exchange
    app.dependency_overrides[login_required] = lambda: None # Bypass auth
    return app

@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)

@pytest.fixture
def mock_allocator():
    """Mock DynamicAllocator."""
    allocator = MagicMock()
    allocator.allocate_capital.return_value = {
        'equity': 0.6,
        'bonds': 0.3,
        'cash': 0.1
    }
    allocator.construct_target_portfolio.return_value = {
        'SPY': 0.6,
        'TLT': 0.3,
        'CASH': 0.1
    }
    return allocator

@pytest.fixture
def mock_risk_monitor():
    """Mock RiskMonitor."""
    monitor = MagicMock()
    monitor.calculate_parametric_var.return_value = 1000.0
    return monitor

@pytest.fixture
def mock_circuit_breaker():
    """Mock CircuitBreaker."""
    breaker = MagicMock()
    breaker.portfolio_frozen = False
    breaker.freeze_reason = None
    breaker.frozen_assets = set()
    return breaker

@pytest.fixture
def mock_paper_exchange():
    """Mock PaperExchange."""
    exchange = MagicMock()
    exchange.get_account_summary.return_value = {
        'cash': 100000.0,
        'total_value': 100000.0,
        'positions': []
    }
    return exchange

def test_get_allocation_success(client, mock_allocator):
    """Test successful allocation retrieval."""
    response = client.get('/api/v1/dashboard/allocation?fear_index=50')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data
    assert 'fear_index' in data['data']
    assert 'buckets' in data['data']
    assert 'target_weights' in data['data']

def test_get_risk_status_success(client, mock_risk_monitor, mock_circuit_breaker, mock_paper_exchange):
    """Test successful risk status retrieval."""
    response = client.get('/api/v1/dashboard/risk')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data
    assert 'var_95_daily' in data['data']
    assert 'portfolio_frozen' in data['data']
    assert 'frozen_assets' in data['data']

def test_get_execution_status_success(client, mock_paper_exchange):
    """Test successful execution status retrieval."""
    response = client.get('/api/v1/dashboard/execution')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'data' in data
    assert 'balance' in data['data'] or 'positions' in data['data']
