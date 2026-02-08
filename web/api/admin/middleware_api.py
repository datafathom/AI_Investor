import logging
from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from services.middleware.pipeline import get_middleware_manager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/middleware", tags=["Admin", "Infrastructure"])

@router.get("/pipeline")
async def get_pipeline_config():
    """Get current request/response interceptor chain."""
    try:
        manager = get_middleware_manager()
        return {"steps": manager.get_pipeline()}
    except Exception as e:
        logger.exception("Error fetching pipeline")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/pipeline")
async def update_pipeline_order(new_order: List[str] = Body(...)):
    """Update execution order of middleware."""
    try:
        manager = get_middleware_manager()
        manager.update_order(new_order)
        return {"status": "success", "message": "Pipeline order updated. Restart required for full effect."}
    except Exception as e:
        logger.exception("Error updating pipeline order")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{middleware_id}")
async def toggle_middleware(middleware_id: str, payload: Dict[str, bool] = Body(...)):
    """Enable or disable specific middleware."""
    try:
        enabled = payload.get("enabled", True)
        manager = get_middleware_manager()
        if manager.toggle_middleware(middleware_id, enabled):
            return {"status": "success", "middleware_id": middleware_id, "enabled": enabled}
        raise HTTPException(status_code=404, detail="Middleware not found")
    except HTTPException: raise
    except Exception as e:
        logger.exception(f"Error toggling middleware {middleware_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_middleware_stats():
    """Get metrics for each middleware step."""
    try:
        manager = get_middleware_manager()
        return manager.get_stats()
    except Exception as e:
        logger.exception("Error fetching middleware stats")
        raise HTTPException(status_code=500, detail=str(e))
