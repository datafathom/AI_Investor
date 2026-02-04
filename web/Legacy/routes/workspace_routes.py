"""Routes for User Workspace Persistence."""
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web.dependencies import get_db, get_current_user  # Assuming these exist in project structure
from services.workspace.user_preferences_service import UserPreferencesService, WorkspaceLayout

router = APIRouter(prefix="/api/v1/user", tags=["Workspace"])

@router.post("/workspace")
async def save_workspace(
    workspace: WorkspaceLayout,
    is_default: bool = False,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save the current workspace layout."""
    service = UserPreferencesService(db)
    workspace_id = await service.save_workspace(user['id'], workspace, is_default)
    return {"status": "success", "workspace_id": workspace_id}

@router.get("/workspace", response_model=WorkspaceLayout)
async def get_workspace(
    name: str = None,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get workspace by name or default."""
    service = UserPreferencesService(db)
    workspace = await service.get_workspace(user['id'], name)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.get("/workspaces")
async def list_workspaces(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all saved workspaces."""
    service = UserPreferencesService(db)
    return await service.list_workspaces(user['id'])

@router.delete("/workspace/{name}")
async def delete_workspace(
    name: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a workspace."""
    service = UserPreferencesService(db)
    deleted = await service.delete_workspace(user['id'], name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"status": "success"}
