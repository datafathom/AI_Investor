
import pytest
from web.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_briefing_endpoint(client):
    rv = client.get('/api/v1/communication/briefing?name=TestUser&fear=10&sentiment=BEARISH')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'briefing_text' in json_data
    assert 'Mr. Anderson' not in json_data['briefing_text'] # Should use TestUser or default if logic changed, but here checking dynamic usage
    assert 'deployment deploying cash' in json_data['briefing_text'].lower() or 'opportunity' in json_data['briefing_text'].lower()

def test_alert_endpoint(client):
    rv = client.post('/api/v1/communication/test-alert', json={
        "message": "API Test",
        "priority": "CRITICAL"
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'sent'
    assert 'SMS' in json_data['channels']
