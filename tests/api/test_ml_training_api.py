"""
Tests for ML Training API Endpoints
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.ml_training_api import router, get_training_pipeline_provider, get_deployment_service_provider
from web.auth_utils import get_current_user


@pytest.fixture
def api_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    # Mock current user
    app.dependency_overrides[get_current_user] = lambda: {'id': 'user_1', 'email': 'test@example.com'}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_pipeline(api_app):
    """Mock Training Pipeline."""
    service = AsyncMock()
    
    job = MagicMock()
    job.model_dump.return_value = {"job_id": "job_123", "status": "created"}
    service.create_training_job.return_value = job
    
    job_started = MagicMock()
    job_started.model_dump.return_value = {"job_id": "job_123", "status": "training"}
    service.start_training.return_value = job_started
    
    job_completed = MagicMock()
    job_completed.model_dump.return_value = {"job_id": "job_123", "status": "completed"}
    service.complete_training.return_value = job_completed
    
    api_app.dependency_overrides[get_training_pipeline_provider] = lambda: service
    return service


@pytest.fixture
def mock_deployment(api_app):
    """Mock Deployment Service."""
    service = AsyncMock()
    
    deployment = MagicMock()
    deployment.model_dump.return_value = {"deployment_id": "dep_123", "status": "deployed"}
    service.deploy_model.return_value = deployment
    
    service.monitor_performance.return_value = {"accuracy": 0.95, "latency": 10}
    
    api_app.dependency_overrides[get_deployment_service_provider] = lambda: service
    return service


def test_create_training_job_success(client, mock_pipeline):
    """Test creating training job."""
    payload = {
        "model_name": "PricePredictor",
        "dataset_id": "ds_001",
        "hyperparameters": {"lr": 0.001}
    }
    response = client.post('/api/v1/ml-training/job/create', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['job_id'] == "job_123"


def test_start_training_success(client, mock_pipeline):
    """Test starting training."""
    response = client.post('/api/v1/ml-training/job/start', json={'job_id': 'job_123'})
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "training"


def test_complete_training_success(client, mock_pipeline):
    """Test completing training."""
    payload = {
        "model_version": {
            "model_id": "mod_001",
            "model_name": "PricePredictor",
            "version": "v1.0.0",
            "framework": "tensorflow",
            "training_status": "completed",
            "accuracy": 0.92,
            "created_date": "2026-02-03T10:00:00"
        }
    }
    response = client.post('/api/v1/ml-training/training/job/job_123/complete', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "completed"


def test_deploy_model_success(client, mock_deployment):
    """Test deploying model."""
    payload = {
        "model_version": {
            "model_id": "mod_001",
            "model_name": "PricePredictor",
            "version": "v1.0.0",
            "framework": "tensorflow",
            "training_status": "completed",
            "accuracy": 0.92,
            "created_date": "2026-02-03T10:00:00"
        },
        "rollout_percentage": 50.0
    }
    response = client.post('/api/v1/ml-training/deploy', json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['status'] == "deployed"


def test_get_performance_success(client, mock_deployment):
    """Test getting performance."""
    response = client.get('/api/v1/ml-training/deployment/mod_001/performance')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['accuracy'] == 0.95
