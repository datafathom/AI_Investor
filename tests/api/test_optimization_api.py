import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime, timezone
from web.api.optimization_api import optimization_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(optimization_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_optimizer_service():
    """Mock PortfolioOptimizerService."""
    with patch('web.api.optimization_api.get_optimizer_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_rebalancing_service():
    """Mock RebalancingService."""
    with patch('web.api.optimization_api.get_rebalancing_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


def test_optimize_portfolio_success(client, mock_optimizer_service):
    """Test successful portfolio optimization."""
    from models.optimization import OptimizationResult
    
    mock_result = OptimizationResult(
        portfolio_id='portfolio_1',
        optimization_method='mean_variance',
        objective='maximize_sharpe',
        optimal_weights={'AAPL': 0.4, 'MSFT': 0.6},
        expected_return=0.12,
        expected_risk=0.15,
        sharpe_ratio=1.5,
        constraint_satisfaction={'min_weight': True, 'max_weight': True},
        optimization_time_seconds=0.5,
        optimization_date=datetime.now(timezone.utc)
    )
    mock_optimizer_service.optimize.return_value = mock_result
    
    response = client.post('/api/optimization/optimize/portfolio_1', 
                           json={'objective': 'maximize_sharpe', 'method': 'mean_variance'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['expected_return'] == 0.12


def test_optimize_portfolio_with_constraints(client, mock_optimizer_service):
    """Test optimization with constraints."""
    from models.optimization import OptimizationResult
    
    mock_result = OptimizationResult(
        portfolio_id='portfolio_1',
        optimization_method='mean_variance',
        objective='maximize_sharpe',
        optimal_weights={'AAPL': 0.4, 'MSFT': 0.6},
        expected_return=0.12,
        expected_risk=0.15,
        sharpe_ratio=1.5,
        constraint_satisfaction={'min_weight': True, 'max_weight': True},
        optimization_time_seconds=0.5,
        optimization_date=datetime.now(timezone.utc)
    )
    mock_optimizer_service.optimize.return_value = mock_result
    
    constraints = {
        'min_weight': 0.1,
        'max_weight': 0.5
    }
    
    response = client.post('/api/optimization/optimize/portfolio_1',
                           json={
                               'objective': 'maximize_sharpe',
                               'method': 'mean_variance',
                               'constraints': constraints
                           })
    
    assert response.status_code == 200
    mock_optimizer_service.optimize.assert_called_once()


def test_optimize_portfolio_error(client, mock_optimizer_service):
    """Test optimization error handling."""
    mock_optimizer_service.optimize.side_effect = Exception('Optimization failed')
    
    response = client.post('/api/optimization/optimize/portfolio_1',
                          json={'objective': 'maximize_sharpe'})
    
    assert response.status_code == 500
    data = response.get_json()
    assert data['success'] is False


def test_check_rebalancing_needed(client, mock_rebalancing_service):
    """Test rebalancing check."""
    mock_rebalancing_service.check_rebalancing_needed.return_value = True
    
    response = client.get('/api/optimization/rebalancing/check/portfolio_1?threshold=0.05')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['needs_rebalancing'] is True


def test_recommend_rebalancing_success(client, mock_rebalancing_service):
    """Test rebalancing recommendation."""
    from models.optimization import RebalancingRecommendation
    
    mock_recommendation = RebalancingRecommendation(
        portfolio_id='portfolio_1',
        current_weights={'AAPL': 0.5, 'MSFT': 0.5},
        target_weights={'AAPL': 0.4, 'MSFT': 0.6},
        recommended_trades=[{'symbol': 'AAPL', 'action': 'sell', 'quantity': 10, 'price': 150.0}],
        drift_percentage=0.1,
        estimated_cost=5.0,
        estimated_tax_impact=2.0,
        requires_approval=False,
        recommendation_date=datetime.now(timezone.utc)
    )
    mock_rebalancing_service.generate_rebalancing_recommendation.return_value = mock_recommendation
    
    response = client.post('/api/optimization/rebalancing/recommend/portfolio_1',
                          json={'strategy': 'threshold'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_execute_rebalancing_success(client, mock_rebalancing_service):
    """Test rebalancing execution."""
    from models.optimization import RebalancingHistory
    
    mock_history = RebalancingHistory(
        rebalancing_id='reb_1',
        portfolio_id='portfolio_1',
        rebalancing_date=datetime.now(timezone.utc),
        strategy='threshold',
        before_weights={'AAPL': 0.5},
        after_weights={'AAPL': 0.4},
        trades_executed=[],
        total_cost=5.0,
        tax_impact=2.0,
        status='executed'
    )
    mock_rebalancing_service.execute_rebalancing.return_value = mock_history
    recommendation_data = {
        'portfolio_id': 'portfolio_1',
        'current_weights': {'AAPL': 0.5},
        'target_weights': {'AAPL': 0.4},
        'recommended_trades': [],
        'drift_percentage': 0.1,
        'estimated_cost': 5.0,
        'estimated_tax_impact': 2.0,
        'requires_approval': False,
        'recommendation_date': datetime.now(timezone.utc).isoformat()
    }
    
    response = client.post('/api/optimization/rebalancing/execute/portfolio_1',
                          json={'recommendation': recommendation_data, 'approved': True})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_execute_rebalancing_missing_recommendation(client):
    """Test rebalancing execution without recommendation."""
    response = client.post('/api/optimization/rebalancing/execute/portfolio_1',
                          json={'approved': True})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_get_rebalancing_history(client, mock_rebalancing_service):
    """Test getting rebalancing history."""
    from models.optimization import RebalancingHistory
    
    mock_history = [
        RebalancingHistory(
            rebalancing_id='reb_1',
            portfolio_id='portfolio_1',
            rebalancing_date=datetime.now(timezone.utc),
            strategy='threshold',
            before_weights={'AAPL': 0.5},
            after_weights={'AAPL': 0.4},
            trades_executed=[],
            total_cost=5.0,
            tax_impact=2.0,
            status='executed'
        )
    ]
    mock_rebalancing_service.get_rebalancing_history.return_value = mock_history
    
    response = client.get('/api/optimization/rebalancing/history/portfolio_1?limit=10')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
