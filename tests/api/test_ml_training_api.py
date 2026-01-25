"""
Tests for ML Training API Endpoints
Phase 27: ML Training & Model Management
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.ml_training_api import ml_training_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(ml_training_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_training_pipeline():
    """Mock TrainingPipeline."""
    with patch('web.api.ml_training_api.get_training_pipeline') as mock:
        pipeline = AsyncMock()
        mock.return_value = pipeline
        yield pipeline


@pytest.fixture
def mock_model_deployment_service():
    """Mock ModelDeploymentService."""
    with patch('web.api.ml_training_api.get_model_deployment_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_training_job_success(client, mock_training_pipeline):
    """Test successful training job creation."""
    from models.ml_training import TrainingJob
    
    mock_job = TrainingJob(
        job_id='job_1',
        model_name='test_model',
        dataset_id='dataset_1',
        status='pending',
        hyperparameters={}
    )
    mock_training_pipeline.create_training_job.return_value = mock_job
    
    response = client.post('/api/ml/training/job/create',
                          json={
                              'model_name': 'test_model',
                              'dataset_id': 'dataset_1',
                              'hyperparameters': {}
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['model_name'] == 'test_model'


@pytest.mark.asyncio
async def test_create_training_job_missing_params(client):
    """Test training job creation with missing parameters."""
    response = client.post('/api/ml/training/job/create',
                          json={'model_name': 'test_model'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_start_training_success(client, mock_training_pipeline):
    """Test successful training start."""
    from models.ml_training import TrainingJob
    
    mock_job = TrainingJob(
        job_id='job_1',
        model_name='test_model',
        dataset_id='dataset_1',
        status='running',
        hyperparameters={}
    )
    mock_training_pipeline.start_training.return_value = mock_job
    
    response = client.post('/api/ml/training/job/job_1/start')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_deploy_model_success(client, mock_model_deployment_service):
    """Test successful model deployment."""
    from models.ml_training import ModelVersion
    
    mock_model = ModelVersion(
        model_id='model_1',
        model_name='test_model',
        version='v1.0',
        status='deployed',
        performance_metrics={}
    )
    mock_model_deployment_service.deploy_model.return_value = mock_model
    
    response = client.post('/api/ml/deployment/deploy',
                          json={
                              'model_id': 'model_1',
                              'version': 'v1.0'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
