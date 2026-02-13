"""
Modes API
Endpoints for system operating modes.
"""
from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict
from services.modes.mode_controller import get_mode_controller

router = APIRouter(prefix="/api/v1/modes", tags=["Modes"])

@router.get("/")
async def list_modes(controller=Depends(get_mode_controller)):
    return {"success": True, "data": controller.list_modes()}

@router.get("/current")
async def get_current_mode(controller=Depends(get_mode_controller)):
    return {"success": True, "data": controller.get_current_mode()}

@router.post("/switch")
async def switch_mode(payload: Dict = Body(...), controller=Depends(get_mode_controller)):
    """
    Expects payload: { "mode": "DEFENSE" }
    """
    mode = payload.get("mode")
    if not mode:
        raise HTTPException(status_code=400, detail="Mode required")
    
    try:
        new_state = controller.switch_mode(mode)
        return {"success": True, "data": new_state}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history")
async def get_mode_history(controller=Depends(get_mode_controller)):
    return {"success": True, "data": controller.get_history()}
