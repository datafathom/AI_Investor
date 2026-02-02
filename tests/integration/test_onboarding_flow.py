"""
Integration Tests: User Onboarding Flow
Tests the complete user onboarding flow
"""

import pytest
from unittest.mock import Mock, patch
from flask import Flask
from web.api.onboarding_api import onboarding_api_bp


@pytest.fixture
def app():
    """Create test Flask app."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(onboarding_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def app_context(app):
    """Push application context."""
    with app.app_context():
        yield


@pytest.fixture
def mock_user():
    """Mock user for testing."""
    user = Mock()
    user.id = 1
    user.email = 'test@example.com'
    return user


class TestOnboardingFlow:
    """Test user onboarding flow."""
    
    @patch('web.api.onboarding_api.g')
    def test_get_onboarding_status(self, mock_g, client, mock_user):
        """Test getting onboarding status."""
        mock_g.user_id = mock_user.id
        
        response = client.get('/api/v1/onboarding/status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'current_step' in data['data']
        assert 'total_steps' in data['data']
    
    @patch('web.api.onboarding_api.g')
    def test_get_onboarding_status_unauthorized(self, mock_g, client):
        """Test getting status without authentication."""
        mock_g.user_id = None
        
        response = client.get('/api/v1/onboarding/status')
        assert response.status_code == 401
    
    @patch('web.api.onboarding_api.g')
    def test_update_onboarding_step(self, mock_g, client, mock_user):
        """Test updating onboarding step."""
        mock_g.user_id = mock_user.id
        
        response = client.post('/api/v1/onboarding/step', json={
            'step': 2,
            'data': {'experience': 'intermediate'}
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['current_step'] == 2
    
    @patch('web.api.onboarding_api.g')
    def test_complete_onboarding(self, mock_g, client, mock_user):
        """Test completing onboarding."""
        mock_g.user_id = mock_user.id
        
        response = client.post('/api/v1/onboarding/complete', json={
            'preferences': {
                'experience_level': 'intermediate',
                'investment_goals': ['growth', 'income'],
                'risk_tolerance': 'moderate',
                'notifications': True,
                'theme': 'dark'
            }
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['completed'] is True
    
    @patch('web.api.onboarding_api.g')
    def test_complete_onboarding_missing_fields(self, mock_g, client, mock_user):
        """Test completing onboarding with missing required fields."""
        mock_g.user_id = mock_user.id
        
        response = client.post('/api/v1/onboarding/complete', json={
            'preferences': {
                'experience_level': 'intermediate'
                # Missing risk_tolerance
            }
        })
        assert response.status_code == 400
    
    @patch('web.api.onboarding_api.g')
    def test_get_preferences(self, mock_g, client, mock_user):
        """Test getting user preferences."""
        mock_g.user_id = mock_user.id
        
        response = client.get('/api/v1/onboarding/preferences')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
    
    @patch('web.api.onboarding_api.g')
    def test_update_preferences(self, mock_g, client, mock_user):
        """Test updating user preferences."""
        mock_g.user_id = mock_user.id
        
        response = client.put('/api/v1/onboarding/preferences', json={
            'preferences': {
                'notifications': False,
                'theme': 'light'
            }
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    @patch('web.api.onboarding_api.g')
    def test_skip_onboarding(self, mock_g, client, mock_user):
        """Test skipping onboarding."""
        mock_g.user_id = mock_user.id
        
        response = client.post('/api/v1/onboarding/skip')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['skipped'] is True
    
    @patch('web.api.onboarding_api.g')
    def test_reset_onboarding(self, mock_g, client, mock_user):
        """Test resetting onboarding."""
        mock_g.user_id = mock_user.id
        
        response = client.post('/api/v1/onboarding/reset')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['reset'] is True
        assert data['data']['current_step'] == 1
