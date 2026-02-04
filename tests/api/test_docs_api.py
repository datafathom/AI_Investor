"""
Tests for Docs API Endpoints
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.docs_api import router


@pytest.fixture
def api_app():
    """Create FastAPI app merchant testing."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


def test_swagger_ui_success(client):
    """Test getting Swagger UI."""
    response = client.get('/api/docs')
    assert response.status_code == 200
    assert "SwaggerUIBundle" in response.text


def test_openapi_json_success(client):
    """Test getting OpenAPI JSON."""
    response = client.get('/api/docs/openapi.json')
    assert response.status_code == 200
    data = response.json()
    assert data['openapi'] == "3.0.0"
    assert data['info']['title'] == "AI Investor API"


def test_redoc_ui_success(client):
    """Test getting ReDoc UI."""
    response = client.get('/api/docs/redoc')
    assert response.status_code == 200
    assert "redoc" in response.text


def test_swagger_yaml_success(client):
    """Test getting Swagger YAML."""
    response = client.get('/api/docs/swagger.yaml')
    assert response.status_code == 200
    assert "openapi: 3.0.0" in response.text
