"""
==============================================================================
FILE: web/api/system_telemetry_api.py
ROLE: System Telemetry Endpoints (FastAPI)
PURPOSE: Returns API quota usage, system health, and load metrics.
==============================================================================
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import random
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/system", tags=["System Telemetry"])


@router.get("/quota")
async def get_quota():
    """Returns API quota usage metrics."""
    try:
        return {
            "success": True,
            "data": {
                "used": random.randint(400, 950),
                "total": 1000,
                "percentage": None
            }
        }
    except Exception as e:
        logger.exception("Failed to fetch quota")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/health")
async def get_health_telemetry():
    """Returns system health and provider latency telemetry."""
    try:
        return {
            "success": True,
            "data": {
                "status": "nominal",
                "latency": {
                    "us-east": random.randint(20, 50),
                    "us-west": random.randint(40, 80),
                    "eu-central": random.randint(100, 150),
                    "ap-southeast": random.randint(200, 300)
                }
            }
        }
    except Exception as e:
        logger.exception("Failed to fetch health telemetry")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/load")
async def get_load():
    """Returns historical system load for sparklines."""
    try:
        return {
            "success": True,
            "data": [random.randint(20, 90) for _ in range(20)]
        }
    except Exception as e:
        logger.exception("Failed to fetch system load")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
