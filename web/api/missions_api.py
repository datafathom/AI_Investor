"""
Missions API
Endpoints for strategic mission planning and tracking.
"""
from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Optional
from services.missions.mission_manager import get_mission_manager

router = APIRouter(prefix="/api/v1/missions", tags=["Missions"])

@router.get("/")
async def list_missions(manager=Depends(get_mission_manager)):
    return {"success": True, "data": manager.list_missions()}

@router.post("/")
async def create_mission(mission_data: Dict = Body(...), manager=Depends(get_mission_manager)):
    mission = manager.create_mission(mission_data)
    return {"success": True, "data": mission}

@router.get("/{mission_id}")
async def get_mission(mission_id: str, manager=Depends(get_mission_manager)):
    mission = manager.get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"success": True, "data": mission}

@router.put("/{mission_id}")
async def update_mission(mission_id: str, updates: Dict = Body(...), manager=Depends(get_mission_manager)):
    mission = manager.update_mission(mission_id, updates)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"success": True, "data": mission}

@router.post("/{mission_id}/milestones")
async def add_milestone(mission_id: str, milestone_data: Dict = Body(...), manager=Depends(get_mission_manager)):
    milestone = manager.add_milestone(mission_id, milestone_data)
    if not milestone:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"success": True, "data": milestone}
