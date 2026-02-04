"""
Tests for Credit Monitoring API Endpoints
Phase 12: Credit Score Monitoring & Improvement
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from web.api.credit_api import router, get_credit_monitoring_provider, get_credit_improvement_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_credit_monitoring_service(api_app):
    """Mock CreditMonitoringService."""
    service = AsyncMock()
    api_app.dependency_overrides[get_credit_monitoring_provider] = lambda: service
    return service


@pytest.fixture
def mock_credit_improvement_service(api_app):
    """Mock CreditImprovementService."""
    service = AsyncMock()
    api_app.dependency_overrides[get_credit_improvement_provider] = lambda: service
    return service


def test_track_credit_score_success(client, mock_credit_monitoring_service):
    """Test successful credit score tracking."""
    from schemas.credit import CreditScore
    
    mock_score = CreditScore(
        score_id='score_1',
        user_id='user_1',
        score=750,
        score_type='fico',
        factors={},
        report_date=datetime.now(timezone.utc)
    )
    mock_credit_monitoring_service.track_credit_score.return_value = mock_score
    
    response = client.post('/api/v1/credit/score/track',
                          json={
                              'user_id': 'user_1',
                              'score': 750,
                              'score_type': 'fico'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['score'] == 750


def test_track_credit_score_missing_params(client):
    """Test credit score tracking with missing parameters."""
    response = client.post('/api/v1/credit/score/track', json={'user_id': 'user_1'})
    
    # Pydantic validation error returns 422
    assert response.status_code == 422


def test_get_credit_history_success(client, mock_credit_monitoring_service):
    """Test successful credit history retrieval."""
    from schemas.credit import CreditScore
    
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
    
    response = client.get('/api/v1/credit/score/history/user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_get_recommendations_success(client, mock_credit_improvement_service):
    """Test successful recommendations retrieval."""
    from schemas.credit import CreditRecommendation
    
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
    mock_credit_improvement_service.generate_recommendations.return_value = mock_recommendations
    
    response = client.get('/api/v1/credit/recommendations/user_1')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
