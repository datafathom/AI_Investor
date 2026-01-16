
import pytest
from web.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_allocation_endpoint(client):
    rv = client.get('/api/v1/dashboard/allocation?fear_index=50')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'buckets' in json_data
    assert json_data['buckets']['ALPHA'] > 0
    assert json_data['buckets']['SHIELD'] > 0

def test_risk_endpoint(client):
    rv = client.get('/api/v1/dashboard/risk')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'var_95_daily' in json_data
    assert 'portfolio_frozen' in json_data

def test_execution_endpoint(client):
    rv = client.get('/api/v1/dashboard/execution')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'balance' in json_data
