"""
Tests for ML Training Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.ml_training import (
    TrainingStatus,
    ModelVersion,
    TrainingJob
)


class TestTrainingStatusEnum:
    """Tests for TrainingStatus enum."""
    
    def test_training_status_enum(self):
        """Test training status enum values."""
        assert TrainingStatus.PENDING == "pending"
        assert TrainingStatus.RUNNING == "running"
        assert TrainingStatus.COMPLETED == "completed"
        assert TrainingStatus.FAILED == "failed"
        assert TrainingStatus.CANCELLED == "cancelled"


class TestModelVersion:
    """Tests for ModelVersion model."""
    
    def test_valid_model_version(self):
        """Test valid model version creation."""
        model = ModelVersion(
            model_id='model_1',
            model_name='price_predictor',
            version='v1.0',
            framework='tensorflow',
            training_status=TrainingStatus.COMPLETED,
            accuracy=0.95,
            created_date=datetime.now(),
            trained_date=datetime.now(),
            metadata={'epochs': 100}
        )
        assert model.model_id == 'model_1'
        assert model.training_status == TrainingStatus.COMPLETED
        assert model.accuracy == 0.95
    
    def test_model_version_defaults(self):
        """Test model version with default values."""
        model = ModelVersion(
            model_id='model_1',
            model_name='test_model',
            version='v1.0',
            framework='pytorch',
            training_status=TrainingStatus.PENDING,
            created_date=datetime.now()
        )
        assert model.accuracy is None
        assert model.trained_date is None
        assert model.metadata == {}


class TestTrainingJob:
    """Tests for TrainingJob model."""
    
    def test_valid_training_job(self):
        """Test valid training job creation."""
        job = TrainingJob(
            job_id='job_1',
            model_name='test_model',
            dataset_id='dataset_1',
            hyperparameters={'learning_rate': 0.001, 'batch_size': 32},
            status=TrainingStatus.RUNNING,
            started_date=datetime.now(),
            completed_date=None,
            error_message=None
        )
        assert job.job_id == 'job_1'
        assert job.status == TrainingStatus.RUNNING
        assert 'learning_rate' in job.hyperparameters
    
    def test_training_job_defaults(self):
        """Test training job with default values."""
        job = TrainingJob(
            job_id='job_1',
            model_name='test_model',
            dataset_id='dataset_1'
        )
        assert job.status == TrainingStatus.PENDING
        assert job.hyperparameters == {}
        assert job.started_date is None
