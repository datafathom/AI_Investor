"""
==============================================================================
FILE: web/api/workspace_api.py
ROLE: Workspace API Endpoints (FastAPI)
PURPOSE: User workspace layout management.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging

from services.workspace.user_preferences_service import get_user_preferences_service, WorkspaceLayout
from web.auth_utils import get_current_user


def get_user_preferences_provider():
    return get_user_preferences_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/user", tags=["Workspace"])


class SaveWorkspaceRequest(BaseModel):
    name: str
    layout: Dict[str, Any]
    panels: List[Dict[str, Any]] = []
    is_default: bool = False


@router.get("/workspace")
async def get_user_workspace(
    name: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_user_preferences_provider)
):
    """Retrieve user workspace layout."""
    user_id = current_user.get("user_id")
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Unauthorized"})
        
    workspace = service.get_workspace(user_id, name)
    
    if workspace:
        return {
            "success": True,
            "data": workspace.model_dump(by_alias=True)
        }
    return JSONResponse(status_code=404, content={"success": False, "detail": "Workspace not found"})


@router.post("/workspace")
async def save_user_workspace(
    request: SaveWorkspaceRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_user_preferences_provider)
):
    """Save user workspace layout."""
    user_id = current_user.get("user_id")
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Unauthorized"})
        
    try:
        workspace = WorkspaceLayout(
            name=request.name,
            layout=request.layout,
            panels=request.panels
        )
        
        ws_id = service.save_workspace(user_id, workspace, request.is_default)
        
        return {
            "success": True,
            "data": {"message": "Workspace saved", "id": ws_id}
        }
    except Exception as e:
        logger.exception("Failed to save workspace")
        return JSONResponse(status_code=400, content={"success": False, "detail": str(e)})


@router.get("/workspaces")
async def list_user_workspaces(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_user_preferences_provider)
):
    """List all workspaces for user."""
    user_id = current_user.get("user_id")
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Unauthorized"})
        
    workspaces = service.list_workspaces(user_id)
    return {
        "success": True,
        "data": workspaces
    }
