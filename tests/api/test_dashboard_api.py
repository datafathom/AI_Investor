"""
Tests for Dashboard API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.dashboard_api import dashboard_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(dashboard_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_allocator():
    """Mock DynamicAllocator."""
    with patch('web.api.dashboard_api.get_dynamic_allocator') as mock:
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
        mock.return_value = allocator
        yield allocator


@pytest.fixture
def mock_risk_monitor():
    """Mock RiskMonitor."""
    with patch('web.api.dashboard_api.get_risk_monitor') as mock:
        monitor = MagicMock()
        monitor.calculate_parametric_var.return_value = 1000.0
        mock.return_value = monitor
        yield monitor


@pytest.fixture
def mock_circuit_breaker():
    """Mock CircuitBreaker."""
    with patch('web.api.dashboard_api.get_circuit_breaker') as mock:
        breaker = MagicMock()
        breaker.portfolio_frozen = False
        breaker.freeze_reason = None
        breaker.frozen_assets = set()
        mock.return_value = breaker
        yield breaker


@pytest.fixture
def mock_paper_exchange():
    """Mock PaperExchange."""
    with patch('web.api.dashboard_api.get_paper_exchange') as mock:
        exchange = MagicMock()
        exchange.get_account_summary.return_value = {
            'cash': 100000.0,
            'total_value': 100000.0
        }
        mock.return_value = exchange
        yield exchange


def test_get_allocation_success(client, mock_allocator):
    """Test successful allocation retrieval."""
    response = client.get('/api/v1/dashboard/allocation?fear_index=50')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'fear_index' in data
    assert 'buckets' in data
    assert 'target_weights' in data


def test_get_risk_status_success(client, mock_risk_monitor, mock_circuit_breaker, mock_paper_exchange):
    """Test successful risk status retrieval."""
    response = client.get('/api/v1/dashboard/risk')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'var_95_daily' in data
    assert 'portfolio_frozen' in data
    assert 'frozen_assets' in data


def test_get_execution_status_success(client, mock_paper_exchange):
    """Test successful execution status retrieval."""
    mock_paper_exchange.get_account_summary.return_value = {
        'cash': 100000.0,
        'total_value': 100000.0,
        'positions': []
    }
    
    response = client.get('/api/v1/dashboard/execution')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'balance' in data or 'total_value' in data
