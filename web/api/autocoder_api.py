"""
==============================================================================
FILE: web/api/autocoder_api.py
ROLE: The Developer Bridge (FastAPI)
PURPOSE: Expose endpoints for AI-driven code generation, validation, and deployment.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
import logging
from typing import List, Optional, Dict, Any
from services.analysis.autocoder import get_autocoder

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dev", tags=["Developer"])


class GenerateRequest(BaseModel):
    task: str = "Default adapter"


class ValidateRequest(BaseModel):
    code: str


class DeployRequest(BaseModel):
    name: str = "temp_module"
    code: str


@router.post('/generate')
async def generate_code(request_data: GenerateRequest):
    """Generate Python code from task description."""
    try:
        coder = get_autocoder()
        code = coder.generate_code(request_data.task)
        
        return {
            "status": "success",
            "task": request_data.task,
            "code": code
        }
    except Exception as e:
        logger.exception("Code generation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/validate')
async def validate_code(request_data: ValidateRequest):
    """Validate Python code AST."""
    try:
        coder = get_autocoder()
        is_valid = coder.validate_code(request_data.code)
        
        return {
            "status": "success" if is_valid else "error",
            "is_valid": is_valid
        }
    except Exception as e:
        logger.exception("Code validation failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/deploy')
async def deploy_module(request_data: DeployRequest):
    """Deploy and hot-swap a Python module."""
    try:
        coder = get_autocoder()
        instance = coder.deploy_module(request_data.name, request_data.code)
        
        if instance:
            return {
                "status": "success",
                "message": f"Module '{request_data.name}' deployed and hot-swapped.",
                "module_name": request_data.name
            }
        else:
            raise HTTPException(
                status_code=400,
                detail={"status": "error", "message": "Deployment failed validation."}
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Deployment failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/status')
async def get_status():
    """Get developer bridge status and module registry."""
    try:
        coder = get_autocoder()
        return {
            "status": "healthy",
            "registry_count": len(coder.registry),
            "modules": list(coder.registry.keys())
        }
    except Exception as e:
        logger.exception("Status check failed")
        raise HTTPException(status_code=500, detail=str(e))
