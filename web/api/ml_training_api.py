"""
==============================================================================
FILE: web/api/ml_training_api.py
ROLE: ML Training API Endpoints
PURPOSE: REST endpoints for ML model training and deployment.

INTEGRATION POINTS:
    - TrainingPipeline: Model training
    - ModelDeploymentService: Model deployment
    - FrontendML: ML operations dashboard

ENDPOINTS:
    - POST /api/ml/training/job/create
    - POST /api/ml/training/job/:job_id/start
    - POST /api/ml/training/job/:job_id/complete
    - POST /api/ml/deployment/deploy
    - GET /api/ml/deployment/:model_id/performance

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.ml.training_pipeline import get_training_pipeline
from services.ml.model_deployment_service import get_model_deployment_service
from models.ml_training import ModelVersion, TrainingStatus

logger = logging.getLogger(__name__)

ml_training_bp = Blueprint('ml_training', __name__, url_prefix='/api/v1/ml')


@ml_training_bp.route('/training/job/create', methods=['POST'])
async def create_training_job():
    """
    Create training job.
    
    Request body:
        model_name: Model name
        dataset_id: Dataset identifier
        hyperparameters: Optional hyperparameters
    """
    try:
        data = request.get_json() or {}
        model_name = data.get('model_name')
        dataset_id = data.get('dataset_id')
        hyperparameters = data.get('hyperparameters')
        
        if not model_name or not dataset_id:
            return jsonify({
                'success': False,
                'error': 'model_name and dataset_id are required'
            }), 400
        
        pipeline = get_training_pipeline()
        job = await pipeline.create_training_job(model_name, dataset_id, hyperparameters)
        
        return jsonify({
            'success': True,
            'data': job.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating training job: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ml_training_bp.route('/training/job/<job_id>/start', methods=['POST'])
async def start_training(job_id: str):
    """
    Start training job.
    """
    try:
        pipeline = get_training_pipeline()
        job = await pipeline.start_training(job_id)
        
        return jsonify({
            'success': True,
            'data': job.dict()
        })
        
    except Exception as e:
        logger.error(f"Error starting training: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ml_training_bp.route('/training/job/<job_id>/complete', methods=['POST'])
async def complete_training(job_id: str):
    """
    Complete training job.
    
    Request body:
        model_version: Model version data
    """
    try:
        data = request.get_json() or {}
        model_data = data.get('model_version')
        
        if not model_data:
            return jsonify({
                'success': False,
                'error': 'model_version is required'
            }), 400
        
        model_version = ModelVersion(**model_data)
        pipeline = get_training_pipeline()
        job = await pipeline.complete_training(job_id, model_version)
        
        return jsonify({
            'success': True,
            'data': job.dict()
        })
        
    except Exception as e:
        logger.error(f"Error completing training: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ml_training_bp.route('/deployment/deploy', methods=['POST'])
async def deploy_model():
    """
    Deploy model.
    
    Request body:
        model_version: Model version data
        rollout_percentage: Rollout percentage (default: 100)
    """
    try:
        data = request.get_json() or {}
        model_data = data.get('model_version')
        rollout_percentage = float(data.get('rollout_percentage', 100))
        
        if not model_data:
            return jsonify({
                'success': False,
                'error': 'model_version is required'
            }), 400
        
        model_version = ModelVersion(**model_data)
        service = get_model_deployment_service()
        deployment = await service.deploy_model(model_version, rollout_percentage)
        
        return jsonify({
            'success': True,
            'data': deployment.dict()
        })
        
    except Exception as e:
        logger.error(f"Error deploying model: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ml_training_bp.route('/deployment/<model_id>/performance', methods=['GET'])
async def get_performance(model_id: str):
    """
    Get model performance metrics.
    """
    try:
        service = get_model_deployment_service()
        performance = await service.monitor_performance(model_id)
        
        return jsonify({
            'success': True,
            'data': performance
        })
        
    except Exception as e:
        logger.error(f"Error getting performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
