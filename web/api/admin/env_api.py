import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from services.system.env_manager import get_env_manager, EnvManager

router = APIRouter(prefix="/env", tags=["Admin", "System"])

class EnvVar(BaseModel):
    key: str
    value: str
    is_sensitive: bool = False
    updated_at: str = "Unknown"

class EnvVarUpdate(BaseModel):
    key: str
    value: str

class BulkEnvUpdate(BaseModel):
    updates: Dict[str, str]

@router.get("", response_model=List[EnvVar])
async def list_env_vars(manager: EnvManager = Depends(get_env_manager)):
    return manager.get_all_vars()

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_env_history(manager: EnvManager = Depends(get_env_manager)):
    return manager.get_history()

@router.post("", response_model=Dict[str, str])
async def update_env_var(update: EnvVarUpdate, manager: EnvManager = Depends(get_env_manager)):
    success = manager.update_var(update.key, update.value)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update environment variable")
    return {"status": "success", "message": f"Updated {update.key}"}

@router.post("/bulk", response_model=Dict[str, str])
async def bulk_update_env_vars(update: BulkEnvUpdate, manager: EnvManager = Depends(get_env_manager)):
    success = manager.bulk_update_vars(update.updates)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update one or more variables")
    return {"status": "success", "message": "Bulk update complete"}
