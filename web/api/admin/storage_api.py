import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from services.infrastructure.private_cloud import get_private_cloud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/storage", tags=["Admin", "Infrastructure"])

@router.get("/pools")
def list_storage_pools():
    """List ZFS storage pools and their status."""
    try:
        cloud = get_private_cloud()
        return cloud.get_pool_status()
    except Exception as e:
        logger.exception("Error listing storage pools")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sync-status")
def get_sync_status():
    """Get status of off-site synchronization."""
    try:
        cloud = get_private_cloud()
        return cloud.get_sync_status()
    except Exception as e:
        logger.exception("Error fetching sync status")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/trigger")
async def trigger_sync():
    """Manually trigger a cloud synchronization."""
    try:
        cloud = get_private_cloud()
        result = await cloud.trigger_sync()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.exception("Error triggering sync")
        raise HTTPException(status_code=500, detail=str(e))
