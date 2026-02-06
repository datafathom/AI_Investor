from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
from services.security.webauthn_service import get_webauthn_service
from services.security.panic_service import get_panic_service

router = APIRouter(prefix="/approvals", tags=["Security | HITL"])

# Schemas
class ApprovalRequest(BaseModel):
    approval_id: str
    signature: str
    public_key: str

class PanicRequest(BaseModel):
    reason: str
    confirmation: str

# Endpoints
@router.get("/pending")
async def get_pending_approvals():
    svc = get_webauthn_service()
    return svc.get_pending_requests()

@router.post("/verify")
async def verify_approval(req: ApprovalRequest):
    svc = get_webauthn_service()
    success = svc.verify_and_approve(req.approval_id, req.signature, req.public_key)
    
    if not success:
        raise HTTPException(status_code=400, detail="Signature verification failed or request invalid.")
    
    return {"status": "approved", "id": req.approval_id}

@router.post("/reject/{approval_id}")
async def reject_approval(approval_id: str):
    svc = get_webauthn_service()
    success = svc.reject_request(approval_id)
    if not success:
        raise HTTPException(status_code=404, detail="Request not found.")
    return {"status": "rejected", "id": approval_id}

@router.post("/panic")
async def trigger_panic(req: PanicRequest):
    if req.confirmation != "I_AM_SURE":
        raise HTTPException(status_code=400, detail="Invalid confirmation.")
    
    svc = get_panic_service()
    await svc.trigger_panic(reason=req.reason)
    return {"status": "system_locked", "message": "Panic Protocol Initiated."}

@router.post("/system/heartbeat")
async def send_heartbeat():
    svc = get_panic_service()
    svc.record_heartbeat()
    return {"status": "alive"}
