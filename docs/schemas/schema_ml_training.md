# Schema: ML Training

## File Location
`schemas/ml_training.py`

## Purpose
Pydantic models for ML model training infrastructure including version management, training job tracking, and performance metrics.

---

## Enums

### TrainingStatus
**Status of ML training job.**

| Value | Description |
|-------|-------------|
| `PENDING` | Queued for training |
| `RUNNING` | Training in progress |
| `COMPLETED` | Training finished successfully |
| `FAILED` | Training failed |
| `CANCELLED` | Training cancelled |

---

## Models

### ModelVersion
**Versioned ML model record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `model_id` | `str` | *required* | Model identifier | Primary key |
| `model_name` | `str` | *required* | Model name | Display |
| `version` | `str` | *required* | Semantic version | Version control |
| `model_type` | `str` | *required* | Type: `prediction`, `classification`, `regression` | Classification |
| `status` | `str` | `"development"` | Status: `development`, `testing`, `production` | Lifecycle |
| `metrics` | `Dict[str, float]` | `{}` | Performance metrics: `{accuracy, f1, mse}` | Evaluation |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `deployed_date` | `Optional[datetime]` | `None` | Production deployment date | Lifecycle |

---

### TrainingJob
**ML training job execution.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `job_id` | `str` | *required* | Unique job identifier | Primary key |
| `model_id` | `str` | *required* | Target model | Links to model |
| `status` | `TrainingStatus` | `PENDING` | Job status | Workflow |
| `hyperparameters` | `Dict` | `{}` | Training hyperparameters | Configuration |
| `dataset_id` | `str` | *required* | Training dataset | Data source |
| `started_date` | `Optional[datetime]` | `None` | Job start time | Timing |
| `completed_date` | `Optional[datetime]` | `None` | Job end time | Timing |
| `metrics` | `Dict[str, float]` | `{}` | Training metrics | Results |
| `logs_url` | `Optional[str]` | `None` | Training logs location | Debugging |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `MLTrainingService` | Training orchestration |
| `ModelRegistryService` | Version management |
| `InferenceService` | Model deployment |

## Frontend Components
- ML dashboard (FrontendML)
- Training job monitor
- Model registry viewer
