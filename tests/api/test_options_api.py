"""
Tests for Options API (FastAPI)
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from web.api.options_api import router as options_router

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(options_router)
    return TestClient(app)

def test_get_options_chain_success(client):
    response = client.get('/api/v1/options/chain?symbol=AAPL')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['symbol'] == 'AAPL'

def test_create_strategy_success(client):
    payload = {
        "strategy_name": "Test Strategy",
        "underlying_symbol": "AAPL",
        "legs": [
            {
                "option_type": "call",
                "strike": 180.0,
                "expiration": "2026-03-21",
                "quantity": 1,
                "action": "buy"
            }
        ]
    }
    response = client.post('/api/v1/options/strategy/create', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['strategy_name'] == "Test Strategy"

def test_create_from_template_success(client):
    payload = {
        "template_name": "covered_call",
        "underlying_symbol": "MSFT",
        "current_price": 400.0,
        "expiration": "2026-04-18"
    }
    response = client.post('/api/v1/options/strategy/template', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']['legs']) == 1

def test_get_greeks_success(client):
    response = client.get('/api/v1/options/strategy/strat_aapl_001/greeks?underlying_price=175.0')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "greeks" in data['data']

def test_get_pnl_success(client):
    response = client.get('/api/v1/options/strategy/strat_aapl_001/pnl?underlying_price=175.0')
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "pnl_at_price" in data['data']

def test_analyze_strategy_success(client):
    payload = {
        "underlying_price": 175.0,
        "days_to_expiration": 30
    }
    response = client.post('/api/v1/options/strategy/strat_aapl_001/analyze', json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert "risk_metrics" in data['data']
