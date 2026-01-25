"""
Tests for Tax API Endpoints
Phase 6: API Endpoint Tests
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from web.api.tax_api import tax_api_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(tax_api_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_taxbit_client():
    """Mock TaxBit client."""
    with patch('web.api.tax_api.get_taxbit_client') as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


def test_get_harvesting_opportunities_success(client, mock_taxbit_client):
    """Test successful tax harvesting opportunities retrieval."""
    mock_opportunities = {
        'opportunities': [
            {'symbol': 'AAPL', 'loss_amount': 1000.0, 'recommendation': 'sell'}
        ]
    }
    
    async def mock_get_opportunities(portfolio_id):
        return mock_opportunities
    
    mock_taxbit_client.get_harvesting_opportunities = mock_get_opportunities
    
    response = client.get('/tax/harvesting/opportunities?mock=true')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'opportunities' in data
