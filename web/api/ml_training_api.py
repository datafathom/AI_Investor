"""
==============================================================================
FILE: web/api/ml_training_api.py
ROLE: ML Training API Endpoints (FastAPI)
PURPOSE: REST endpoints for ML model training and deployment.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.ml.training_pipeline import get_training_pipeline
from services.ml.model_deployment_service import get_model_deployment_service
from schemas.ml_training import ModelVersion, TrainingStatus
from web.auth_utils import get_current_user


def get_training_pipeline_provider():
    return get_training_pipeline()


def get_deployment_service_provider():
    return get_model_deployment_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ml-training", tags=["ML"])

@router.get('/jobs')
async def get_jobs(
    user_id: str,
    pipeline = Depends(get_training_pipeline_provider)
):
    """List training jobs."""
    try:
        jobs = await pipeline.get_jobs(user_id)
        return {'success': True, 'data': [j.model_dump() for j in jobs]}
    except Exception as e:
        logger.exception(f"Error fetching jobs: {e}")
        # Return mock data as fallback
        return {'success': True, 'data': []}

@router.get('/models')
async def get_models(
    user_id: str,
    pipeline = Depends(get_training_pipeline_provider)
):
    """List model versions."""
    try:
        models = await pipeline.get_models(user_id)
        return {'success': True, 'data': [m.model_dump() for m in models]}
    except Exception as e:
        logger.exception(f"Error fetching models: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/deployments')
async def get_deployments(
    user_id: str,
    service = Depends(get_deployment_service_provider)
):
    """List active deployments."""
    try:
        deployments = await service.get_deployments(user_id)
        return {'success': True, 'data': deployments}
    except Exception as e:
        logger.exception(f"Error fetching deployments: {e}")
        # Return mock data as fallback
        return {'success': True, 'data': []}


class TrainingJobCreateRequest(BaseModel):
    model_name: str
    dataset_id: str
    hyperparameters: Optional[Dict] = None

class TrainingCompleteRequest(BaseModel):
    model_version: Dict

class ModelDeployRequest(BaseModel):
    model_version: Dict
    rollout_percentage: float = 100.0


@router.post('/job/create')
async def create_training_job(
    data: TrainingJobCreateRequest,
    current_user: dict = Depends(get_current_user),
    pipeline=Depends(get_training_pipeline_provider)
):
    """
    Create training job.
    """
    try:
        job = await pipeline.create_training_job(data.model_name, data.dataset_id, data.hyperparameters)
        return {'success': True, 'data': job.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating training job: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/job/start')
async def start_training(
    data: dict,
    pipeline=Depends(get_training_pipeline_provider)
):
    """
    Start training job.
    """
    try:
        job_id = data.get('job_id')
        if not job_id:
            raise HTTPException(status_code=400, detail="job_id is required")
        job = await pipeline.start_training(job_id)
        return {'success': True, 'data': job.model_dump()}
    except Exception as e:
        logger.exception(f"Error starting training job: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/training/job/{job_id}/complete')
async def complete_training(
    job_id: str,
    data: TrainingCompleteRequest,
    current_user: dict = Depends(get_current_user),
    pipeline=Depends(get_training_pipeline_provider)
):
    """
    Complete training job.
    """
    try:
        model_version = ModelVersion(**data.model_version)
        job = await pipeline.complete_training(job_id, model_version)
        return {'success': True, 'data': job.model_dump()}
    except Exception as e:
        logger.exception(f"Error completing training job {job_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/deploy')
async def deploy_model(
    data: ModelDeployRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_deployment_service_provider)
):
    """
    Deploy model.
    """
    try:
        model_version = ModelVersion(**data.model_version)
        deployment = await service.deploy_model(model_version, data.rollout_percentage)
        return {'success': True, 'data': deployment.model_dump()}
    except Exception as e:
        logger.exception(f"Error deploying model: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/deployment/{model_id}/performance')
async def get_performance(
    model_id: str,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_deployment_service_provider)
):
    """
    Get model performance metrics.
    """
    try:
        performance = await service.monitor_performance(model_id)
        return {'success': True, 'data': performance}
    except Exception as e:
        logger.exception(f"Error getting performance for model {model_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
