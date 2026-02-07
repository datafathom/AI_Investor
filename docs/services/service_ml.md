# Backend Service: ML (Machine Learning Pipeline)

## Overview
The **ML Service** provides the end-to-end MLOps infrastructure for the platform. It manages the complete lifecycle of predictive models—from data ingestion and training to versioning, A/B testing, and production deployment. The service is designed to support both classical ML (XGBoost, RandomForest) and deep learning workflows, ensuring that the AI Investor's decision-making engines are continuously retrained and improved without downtime.

## Core Components

### 1. Training Pipeline Orchestrator (`training_pipeline.py`)
Manages the model creation lifecycle.
- **Job Scheduling**: Creates and tracks training jobs with specific datasets and hyperparameter configurations. It maintains a ledger of all training attempts (`PENDING` -> `RUNNING` -> `COMPLETED`) to ensure reproducibility.
- **Model Versioning**: Automatically fingerprints and versions every trained model artifact. This ensures that the system can always roll back to a previous "Golden Master" if a newer model shows performance degradation.

### 2. Model Deployment Service (`model_deployment_service.py`)
Handles the transition from training to inference.
- **Gradual Rollouts**: Supports "Canary Deployments" where a new model version is rolled out to only a small percentage (e.g., 5%) of inference requests. This allows for safe A/B testing against live market data.
- **Performance Monitoring**: Tracks key metrics like inference latency, throughput, and accuracy in real-time.
- **Instant Rollback**: Provides a "Kill Switch" to immediately revert to the previous stable model version if the error rate spikes.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **System Monitor** | Tensor Monitor | `model_deployment_service.monitor_performance()` | **Implemented** (`TensorMonitor.jsx`) |
| **Admin Console** | Model Version Grid | `training_pipeline.get_job()` | **Missing** |
| **Admin Console** | Deployment Rollout Slider | `model_deployment_service.deploy_model()` | **Missing** |

> [!NOTE]
> **Integration Status**: While the `TensorMonitor` widget exists for visualizing model performance, the administrative controls for triggering training jobs or managing deployment rollouts are currently **Backend-Only**. These operations must be performed via API or CLI.

## Dependencies
- `schemas.ml_training`: Defines standard models for `TrainingJob`, `ModelVersion`, and `TrainingStatus`.
- `services.system.cache_service`: Persists job status and deployment configurations.

## Usage Examples

### Starting a New Training Job
```python
from services.ml.training_pipeline import get_training_pipeline

pipeline = get_training_pipeline()

# Launch a training run for the "Price_Predictor_v2" model
job = await pipeline.create_training_job(
    model_name="Price_Predictor_LSTM",
    dataset_id="dataset_market_2025_Q4",
    hyperparameters={"epochs": 50, "batch_size": 32, "learning_rate": 0.001}
)

# Start the job (Async)
started_job = await pipeline.start_training(job_id=job.job_id)
print(f"Training Started: {started_job.job_id} at {started_job.started_date}")
```

### Deploying a Canary Version (10% Traffic)
```python
from services.ml.model_deployment_service import get_model_deployment_service

deployment_svc = get_model_deployment_service()

# Deploy model version 'v1.2.5' to 10% of users
result = await deployment_svc.deploy_model(
    model_version=my_model_object,
    rollout_percentage=10.0
)

print(f"Deployment Active: {result['deployment_id']}")
print(f"Rollout: {result['rollout_percentage']}%")
```

### Emergency Rollback
```python
from services.ml.model_deployment_service import get_model_deployment_service

svc = get_model_deployment_service()

# Revert to previous stable version
success = await svc.rollback_model(model_id="Price_Predictor_LSTM")

if success:
    print("Rollback successful. Traffic redirected to previous version.")
```
