"""
==============================================================================
FILE: web/api/health_api.py
ROLE: Enhanced Health Check API (FastAPI)
PURPOSE: Production-ready health checks for load balancers and monitoring
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import timezone, datetime
import logging
import asyncio

from services.system.health_check_service import get_health_check_service
from services.security.system_health_service import get_system_health_service


def get_health_check_provider():
    return get_health_check_service()


def get_system_health_provider():
    return get_system_health_service()

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health")
@router.get("/api/health")
async def health_check():
    """
    Basic health check endpoint.
    Returns 200 if service is up, used by load balancers.
    """
    return {
        "success": True,
        "data": {
            'status': 'healthy',
            'service': 'ai-investor-backend',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    }


@router.get("/health/readiness")
async def readiness_check(
    health_service = Depends(get_health_check_provider)
):
    """
    Readiness check - verifies service can accept traffic.
    Checks database connectivity.
    """
    try:
        postgres_status = await asyncio.to_thread(health_service.check_postgres)
        redis_status = await asyncio.to_thread(health_service.check_redis)
        
        if postgres_status.get('status') == 'UP' and redis_status.get('status') == 'UP':
            return {
                "success": True,
                "data": {
                    'status': 'ready',
                    'checks': {
                        'postgres': postgres_status,
                        'redis': redis_status
                    },
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "success": False,
                    "detail": "Service dependencies not ready",
                    "data": {
                        'status': 'not_ready',
                        'checks': {
                            'postgres': postgres_status,
                            'redis': redis_status
                        },
                        'timestamp': datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
    except Exception as e:
        logger.exception("Readiness check failed")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "detail": str(e),
                "data": {
                    'status': 'not_ready',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            }
        )


@router.get("/health/liveness")
async def liveness_check():
    """
    Liveness check - verifies service is alive.
    Should be fast and not check dependencies.
    """
    return {
        "success": True,
        "data": {
            'status': 'alive',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    }


@router.get("/health/detailed")
async def detailed_health(
    health_service = Depends(get_health_check_provider),
    system_health_service = Depends(get_system_health_provider)
):
    """
    Detailed health check with full system status.
    Used for monitoring dashboards.
    """
    try:
        system_status = await asyncio.to_thread(system_health_service.get_health_status)
        pg_status = await asyncio.to_thread(health_service.check_postgres)
        rd_status = await asyncio.to_thread(health_service.check_redis)

        return {
            "success": True,
            "data": {
                'status': 'healthy',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'checks': {
                    'postgres': pg_status,
                    'redis': rd_status,
                    'system': system_status
                }
            }
        }
        
    except Exception as e:
        logger.exception("Detailed health check failed")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "detail": str(e),
                "data": {
                    'status': 'unhealthy',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            }
        )
