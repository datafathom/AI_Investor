import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel

from services.system.feature_flags import get_feature_flag_manager, FeatureFlagManager

router = APIRouter(prefix="/features", tags=["Admin", "Feature Flags"])

class FlagUpdate(BaseModel):
    enabled: Optional[bool] = None
    percentage: Optional[float] = None
    targeting: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = None

class FlagEvaluation(BaseModel):
    name: str
    context: Dict[str, Any] = {}

# --- Dependency ---

def get_manager():
    return get_feature_flag_manager()

# --- Endpoints ---

@router.get("", response_model=Dict[str, Any])
async def list_flags(manager: FeatureFlagManager = Depends(get_manager)):
    return manager.get_all_flags()

@router.post("/evaluate", response_model=Dict[str, bool])
async def evaluate_flag(request: FlagEvaluation, manager: FeatureFlagManager = Depends(get_manager)):
    result = manager.evaluate_flag(request.name, request.context)
    return {"enabled": result}

@router.post("/{name}", response_model=Dict[str, str])
async def update_flag(name: str, updates: FlagUpdate, manager: FeatureFlagManager = Depends(get_manager)):
    success = manager.update_flag(name, updates.dict(exclude_unset=True))
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update flag")
    return {"status": "success", "message": f"Updated flag {name}"}

@router.post("/{name}/toggle", response_model=Dict[str, str])
async def toggle_flag(name: str, manager: FeatureFlagManager = Depends(get_manager)):
    if manager.toggle_flag(name):
        return {"status": "success", "message": f"Toggled flag {name}"}
    raise HTTPException(status_code=404, detail="Flag not found")
