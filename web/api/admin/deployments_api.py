import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from services.blue_green.controller import get_blue_green_controller

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/deployments", tags=["Admin", "Deployments"])

# --- Pydantic Models ---

class TrafficSplitRequest(BaseModel):
    blue: int
    green: int

class SwitchRequest(BaseModel):
    target_env: str

class EnvironmentStatus(BaseModel):
    version: str
    status: str
    last_deployed: str

class DeploymentState(BaseModel):
    active_env: str
    traffic_split: Dict[str, int]
    environments: Dict[str, EnvironmentStatus]
    history: List[Dict[str, Any]]

# --- Endpoints ---

@router.get("/environments")
async def get_environments():
    """List blue/green environments."""
    try:
        controller = get_blue_green_controller()
        status = controller.get_status()
        return status["environments"]
    except Exception as e:
        logger.exception("Failed to get environments")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current")
async def get_current_deployment():
    """Get the currently active environment."""
    try:
        controller = get_blue_green_controller()
        status = controller.get_status()
        return {
            "active_env": status["active_env"],
            "traffic_split": status["traffic_split"]
        }
    except Exception as e:
        logger.exception("Failed to get current deployment")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_deployment_history():
    """Get deployment change history."""
    try:
        controller = get_blue_green_controller()
        status = controller.get_status()
        return status["history"]
    except Exception as e:
        logger.exception("Failed to get history")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=DeploymentState)
async def get_status():
    """Get current blue/green deployment status (Legacy/Combined)."""
    try:
        controller = get_blue_green_controller()
        return controller.get_status()
    except Exception as e:
        logger.exception("Failed to get deployment status")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/switch")
async def switch_environment(request: SwitchRequest):
    """Switch active environment (100% traffic)."""
    try:
        controller = get_blue_green_controller()
        return controller.switch_environment(request.target_env)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Failed to switch environment")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/traffic")
async def update_traffic_split(request: TrafficSplitRequest):
    """Update traffic split percentages."""
    try:
        controller = get_blue_green_controller()
        return controller.set_traffic_split(request.blue, request.green)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Failed to update traffic split")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rollback")
async def rollback_deployment():
    """Rollback to the previous stable environment."""
    try:
        controller = get_blue_green_controller()
        return controller.rollback()
    except Exception as e:
        logger.exception("Failed to rollback deployment")
        raise HTTPException(status_code=500, detail=str(e))
