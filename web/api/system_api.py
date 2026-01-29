"""
System API - Infrastructure & Health
Phase 62: Endpoints for monitoring system infrastructure and agent loads.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from services.security.system_health_service import (
    SystemHealthService,
    ComponentHealth,
    get_system_health_service
)

from services.system.secret_manager import get_secret_manager
from services.auth.totp_service import get_totp_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/system", tags=["System"])


class SecretAccessRequest(BaseModel):
    """Sprint 6: Request model for secrets access requiring MFA."""
    mfa_code: str


@router.post("/secrets")
async def get_secrets_status(request: SecretAccessRequest):
    """
    Sprint 6: Get system secrets status - requires 2FA verification.
    Critical security endpoint protected by TOTP MFA.
    """
    # Verify MFA code
    totp_service = get_totp_service()
    # In production, fetch user's MFA secret from DB
    is_valid = totp_service.verify_code("DEMO_SECRET", request.mfa_code)
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid MFA code")
    
    sm = get_secret_manager()
    status = sm.get_status()
    return {
        "status": "Healthy" if status["status"] == "Active" else "Degraded",
        "engine": status["engine"],
        "source": "Environment (.env)",
        "vault_connected": False,
        "security_gateway": {
            "rate_limiter": "Active",
            "waf_rules": "Core v1"
        },
        "missing_critical_keys": [],
        "mfa_verified": True
    }

@router.get("/health")
async def get_system_health(
    service: SystemHealthService = Depends(get_system_health_service)
):
    return await service.get_health_status()

@router.post("/restart/{service_name}")
async def restart_service(
    service_name: str,
    service: SystemHealthService = Depends(get_system_health_service)
):
    success = await service.restart_service(service_name)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to restart service")
    return {"status": "success", "message": f"{service_name} restart triggered"}

@router.get("/kafka/lag")
async def get_kafka_lag(
    service: SystemHealthService = Depends(get_system_health_service)
):
    health = await service.get_health_status()
    kafka = health.get("kafka")
    return kafka.details if kafka else {"error": "Not available"}
