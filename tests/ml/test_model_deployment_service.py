"""
Tests for Model Deployment Service
Comprehensive test coverage for model deployment, A/B testing, and rollback
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.ml.model_deployment_service import ModelDeploymentService
from schemas.ml_training import ModelVersion


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.ml.model_deployment_service.get_cache_service'):
        return ModelDeploymentService()


@pytest.fixture
def mock_model_version():
    """Mock model version."""
    from schemas.ml_training import TrainingStatus
    return ModelVersion(
        model_id="model_123",
        model_name="price_predictor",
        version="v1.0",
        framework="tensorflow",
        training_status=TrainingStatus.COMPLETED,
        accuracy=0.85,
        created_date=datetime.now(timezone.utc),
        metadata={'training_job_id': 'job_123'}
    )


@pytest.mark.asyncio
async def test_deploy_model(service, mock_model_version):
    """Test model deployment."""
    result = await service.deploy_model(
        model_version=mock_model_version,
        rollout_percentage=100.0
    )
    
    assert result is not None
    assert result['model_id'] == "model_123"
    assert result['rollout_percentage'] == 100.0
    assert result['status'] == "active"
    assert mock_model_version.model_id in service.deployed_models


@pytest.mark.asyncio
async def test_deploy_model_gradual_rollout(service, mock_model_version):
    """Test gradual rollout deployment."""
    result = await service.deploy_model(
        model_version=mock_model_version,
        rollout_percentage=25.0  # 25% rollout
    )
    
    assert result is not None
    assert result['rollout_percentage'] == 25.0


@pytest.mark.asyncio
async def test_monitor_performance(service, mock_model_version):
    """Test performance monitoring."""
    service.deployed_models[mock_model_version.model_id] = mock_model_version
    service._collect_metrics = AsyncMock(return_value={
        'accuracy': 0.85,
        'latency_ms': 50,
        'throughput': 1000
    })
    
    result = await service.monitor_performance("model_123")
    
    assert result is not None
    assert 'accuracy' in result or hasattr(result, 'accuracy')


@pytest.mark.asyncio
async def test_rollback_model(service, mock_model_version):
    """Test model rollback."""
    service.deployed_models[mock_model_version.model_id] = mock_model_version
    service._remove_deployment = AsyncMock(return_value=True)
    
    result = await service.rollback_model("model_123")
    
    assert result is True
    assert "model_123" not in service.deployed_models
