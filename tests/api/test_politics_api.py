"""
Tests for Politics API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.politics_api import politics_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(politics_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_congress_tracker():
    """Mock CongressTracker."""
    with patch('web.api.politics_api.get_congress_tracker') as mock:
        tracker = MagicMock()
        tracker.fetch_latest_disclosures.return_value = [
            {'politician': 'John Doe', 'ticker': 'AAPL', 'action': 'buy', 'amount': 10000}
        ]
        tracker.get_political_alpha_signal.return_value = 0.75
        tracker.correlate_with_lobbying.return_value = {
            'lobbying_intensity': 0.6,
            'confidence': 0.8
        }
        mock.return_value = tracker
        yield tracker


def test_get_disclosures_success(client, mock_congress_tracker):
    """Test successful disclosures retrieval."""
    response = client.get('/api/v1/politics/disclosures')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'data' in data
    assert 'count' in data


def test_get_alpha_score_success(client, mock_congress_tracker):
    """Test successful alpha score retrieval."""
    response = client.get('/api/v1/politics/alpha/AAPL')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'ticker' in data
    assert 'alpha_score' in data
    assert 'lobbying_intensity' in data
