"""
Tests for Fixed Income API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.fixed_income_api import router


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_get_yield_curve_success(client):
    """Test successful yield curve retrieval."""
    response = client.get('/api/v1/fixed-income/yield-curve')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'rates' in data['data']


def test_get_yield_curve_history_success(client):
    """Test successful yield curve history retrieval."""
    response = client.get('/api/v1/fixed-income/yield-curve/history?months=6')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert isinstance(data['data'], list)


def test_simulate_rate_shock_success(client):
    """Test successful rate shock simulation."""
    response = client.post('/api/v1/fixed-income/rate-shock',
                          json={'portfolio_id': 'test', 'basis_points': 100})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'shock_basis_points' in data['data']


def test_calculate_duration_success(client):
    """Test successful duration calculation."""
    response = client.post('/api/v1/fixed-income/duration',
                          json={'par_value': 1000, 'coupon_rate': 0.05, 'maturity_years': 5, 'ytm': 0.05})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'macaulay_duration' in data['data']


def test_check_inversion_success(client):
    """Test successful yield curve inversion check."""
    response = client.get('/api/v1/fixed-income/inversion')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 'is_inverted' in data['data']
