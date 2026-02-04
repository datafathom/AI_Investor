"""
==============================================================================
FILE: models/ml_training.py
ROLE: ML Training Data Models
PURPOSE: Pydantic models for ML model training, deployment, and monitoring.

INTEGRATION POINTS:
    - TrainingPipeline: Model training
    - ModelDeploymentService: Model deployment
    - MLTrainingAPI: ML training endpoints
    - FrontendML: ML operations dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class TrainingStatus(str, Enum):
    """Training status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ModelVersion(BaseModel):
    """Model version definition."""
    model_id: str
    model_name: str
    version: str
    framework: str  # tensorflow, pytorch, sklearn
    training_status: TrainingStatus
    accuracy: Optional[float] = None
    created_date: datetime
    trained_date: Optional[datetime] = None
    metadata: Dict = {}


class TrainingJob(BaseModel):
    """Training job definition."""
    job_id: str
    model_name: str
    dataset_id: str
    hyperparameters: Dict = {}
    status: TrainingStatus = TrainingStatus.PENDING
    started_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    error_message: Optional[str] = None
