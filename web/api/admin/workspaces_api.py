import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel

from services.workspaces.manager import get_workspace_manager, WorkspaceManager

router = APIRouter(prefix="/workspaces", tags=["Admin", "Workspaces"])

# --- Pydantic Models ---

class UserAssignment(BaseModel):
    user_id: str
    role: str

class QuotaUpdates(BaseModel):
    storage_gb: Optional[float] = None
    api_calls_day: Optional[int] = None
    concurrent_sessions: Optional[int] = None

class WorkspaceCreate(BaseModel):
    name: str
    layout: Dict[str, Any] = {"type": "default"}

# --- Dependency ---

def get_manager():
    return get_workspace_manager()

# --- Endpoints ---

@router.get("", response_model=List[Dict[str, Any]])
async def list_workspaces(manager: WorkspaceManager = Depends(get_manager)):
    return manager.list_workspaces()

@router.post("", response_model=Dict[str, Any])
async def create_workspace(request: WorkspaceCreate, manager: WorkspaceManager = Depends(get_manager)):
    return manager.create_workspace(request.name, request.layout)

@router.get("/{workspace_id}", response_model=Dict[str, Any])
async def get_workspace(workspace_id: str, manager: WorkspaceManager = Depends(get_manager)):
    ws = manager.get_workspace(workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return ws

@router.post("/{workspace_id}/users", response_model=Dict[str, str])
async def assign_user(workspace_id: str, assignment: UserAssignment, manager: WorkspaceManager = Depends(get_manager)):
    success = manager.assign_user(workspace_id, assignment.user_id, assignment.role)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"status": "success", "message": f"User {assignment.user_id} assigned"}

@router.delete("/{workspace_id}/users/{user_id}", response_model=Dict[str, str])
async def remove_user(workspace_id: str, user_id: str, manager: WorkspaceManager = Depends(get_manager)):
    success = manager.remove_user(workspace_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace or user not found")
    return {"status": "success", "message": f"User {user_id} removed"}

@router.patch("/{workspace_id}/quotas", response_model=Dict[str, str])
async def update_quotas(workspace_id: str, updates: QuotaUpdates, manager: WorkspaceManager = Depends(get_manager)):
    success = manager.update_quotas(workspace_id, updates.dict(exclude_unset=True))
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return {"status": "success", "message": "Quotas updated"}

@router.delete("/{workspace_id}", response_model=Dict[str, str])
async def delete_workspace(workspace_id: str, manager: WorkspaceManager = Depends(get_manager)):
    if manager.delete_workspace(workspace_id):
        return {"status": "success", "message": f"Deleted workspace {workspace_id}"}
    raise HTTPException(status_code=404, detail="Workspace not found")
