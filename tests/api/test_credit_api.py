"""
Tests for Credit Monitoring API Endpoints
Phase 12: Credit Score Monitoring & Improvement
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from datetime import datetime, timezone
from web.api.credit_api import credit_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(credit_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_credit_monitoring_service():
    """Mock CreditMonitoringService."""
    with patch('web.api.credit_api.get_credit_monitoring_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_credit_improvement_service():
    """Mock CreditImprovementService."""
    with patch('web.api.credit_api.get_credit_improvement_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


def test_track_credit_score_success(client, mock_credit_monitoring_service):
    """Test successful credit score tracking."""
    from models.credit import CreditScore
    
    mock_score = CreditScore(
        score_id='score_1',
        user_id='user_1',
        score=750,
        score_type='fico',
        factors={},
        report_date=datetime.now(timezone.utc)
    )
    mock_credit_monitoring_service.track_credit_score.return_value = mock_score
    
    response = client.post('/api/credit/score/track',
                          json={
                              'user_id': 'user_1',
                              'score': 750,
                              'score_type': 'fico'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['score'] == 750


def test_track_credit_score_missing_params(client):
    """Test credit score tracking with missing parameters."""
    response = client.post('/api/credit/score/track', json={'user_id': 'user_1'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_get_credit_history_success(client, mock_credit_monitoring_service):
    """Test successful credit history retrieval."""
    from models.credit import CreditScore
    
    mock_scores = [
        CreditScore(
            score_id='score_1',
            user_id='user_1',
            score=750,
            score_type='fico',
            factors={},
            report_date=datetime.now(timezone.utc)
        )
    ]
    mock_credit_monitoring_service.get_credit_history.return_value = mock_scores
    
    response = client.get('/api/credit/score/history/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_recommendations_success(client, mock_credit_improvement_service):
    """Test successful recommendations retrieval."""
    from models.credit import CreditRecommendation
    
    mock_recommendations = [
        CreditRecommendation(
            recommendation_id='rec_1',
            factor='credit_utilization',
            title='Pay Down Debt',
            description='Reducing your credit utilization will increase your score.',
            impact_score=20,
            difficulty='medium',
            estimated_time='1 month',
            action_items=['Pay off credit card balance']
        )
    ]
    mock_credit_improvement_service.get_recommendations.return_value = mock_recommendations
    
    response = client.get('/api/credit/recommendations/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
