"""
Tests for ML Training Pipeline
Comprehensive test coverage for training jobs and model versioning
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.ml.training_pipeline import TrainingPipeline
from models.ml_training import TrainingJob, TrainingStatus, ModelVersion


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.ml.training_pipeline.get_cache_service'):
        return TrainingPipeline()


@pytest.mark.asyncio
async def test_create_training_job(service):
    """Test training job creation."""
    service._save_job = AsyncMock()
    
    result = await service.create_training_job(
        model_name="price_predictor",
        dataset_id="dataset_123",
        hyperparameters={'learning_rate': 0.001, 'epochs': 100}
    )
    
    assert result is not None
    assert isinstance(result, TrainingJob)
    assert result.model_name == "price_predictor"
    assert result.status == TrainingStatus.PENDING


@pytest.mark.asyncio
async def test_start_training(service):
    """Test starting training job."""
    job = TrainingJob(
        job_id="job_123",
        model_name="price_predictor",
        dataset_id="dataset_123",
        hyperparameters={},
        status=TrainingStatus.PENDING
    )
    
    service._get_job = AsyncMock(return_value=job)
    service._execute_training = AsyncMock(return_value={'status': 'training'})
    service._save_job = AsyncMock()
    
    result = await service.start_training("job_123")
    
    assert result is not None
    assert result.status == TrainingStatus.TRAINING


@pytest.mark.asyncio
async def test_get_model_versions(service):
    """Test getting model versions."""
    service._get_versions_from_db = AsyncMock(return_value=[
        ModelVersion(
            version_id="v1.0",
            model_name="price_predictor",
            training_job_id="job_123",
            performance_metrics={'accuracy': 0.85},
            created_date=datetime.utcnow()
        )
    ])
    
    result = await service.get_model_versions("price_predictor")
    
    assert result is not None
    assert len(result) == 1
