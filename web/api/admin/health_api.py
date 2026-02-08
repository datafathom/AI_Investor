import logging
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from services.system.health_check_service import get_health_check_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["Admin", "Infrastructure"])

@router.get("/services")
async def list_health_services():
    """List all services with their current health status."""
    try:
        svc = get_health_check_service()
        return svc.get_full_status()
    except Exception as e:
        logger.exception("Error fetching service health")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/{service_id}")
async def get_service_details(service_id: str):
    """Get detailed health info for a specific service."""
    try:
        svc = get_health_check_service()
        # For now, just trigger a check
        return svc.trigger_health_check(service_id)
    except Exception as e:
        logger.exception(f"Error fetching details for {service_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/{service_id}/history")
async def get_service_history(service_id: str):
    """Get 30-day uptime history for a service."""
    try:
        svc = get_health_check_service()
        return svc.get_uptime_history(service_id)
    except Exception as e:
        logger.exception(f"Error fetching history for {service_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/services/{service_id}/check")
async def manual_health_check(service_id: str):
    """Trigger a manual health check."""
    try:
        svc = get_health_check_service()
        return svc.trigger_health_check(service_id)
    except Exception as e:
        logger.exception(f"Error triggering check for {service_id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dependencies")
async def get_dependency_map():
    """Get the service dependency graph."""
    try:
        svc = get_health_check_service()
        return svc.get_dependency_map()
    except Exception as e:
        logger.exception("Error fetching dependency map")
        raise HTTPException(status_code=500, detail=str(e))
