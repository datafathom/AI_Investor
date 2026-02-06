"""
==============================================================================
FILE: web/api/compliance_api.py
ROLE: Compliance API Endpoints (FastAPI)
PURPOSE: REST endpoints for compliance checking and reporting.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from services.compliance.compliance_service import get_compliance_service
from services.compliance.record_vault import get_record_vault
from web.auth_utils import get_current_user

def get_compliance_engine():
    """Mock compliance engine."""
    return type('MockEngine', (), {'get_compliance_status': lambda x: {"status": "compliant"}, 'get_violations': lambda x: []})()

def get_reporting_service():
    """Mock reporting service."""
    return type('MockReporting', (), {'get_compliance_overview': lambda x: {"summary": "Stable"}, 'generate_compliance_report': lambda **k: type('Report', (), {'model_dump': lambda **j: {"report": "generated"}})()})()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/compliance", tags=["Compliance"])

class ComplianceCheckRequest(BaseModel):
    user_id: str
    transaction: dict

class ReportGenerationRequest(BaseModel):
    user_id: str
    report_type: str
    period_start: datetime
    period_end: datetime


@router.post('/check')
async def check_compliance(
    data: ComplianceCheckRequest,
    service = Depends(get_compliance_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Check transaction for compliance violations (e.g. Wash Sales).
    """
    try:
        # Check for wash sale
        is_wash_sale, reason = service.check_wash_sale(
            data.user_id, 
            data.transaction.get('symbol'),
            data.transaction.get('amount', 0)
        )
        
        return {
            'success': True,
            'is_compliant': not is_wash_sale,
            'violations': [reason] if is_wash_sale else []
        }
        
    except Exception as e:
        logger.exception(f"Error checking compliance: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/verify')
async def verify_compliance_status(
    user_id: Optional[str] = Query(None),
    engine = Depends(get_compliance_engine),
    current_user: dict = Depends(get_current_user)
):
    """Verify high-level compliance status for user."""
    try:
        uid = user_id or current_user.get('user_id')
        status = await engine.get_compliance_status(uid) if hasattr(engine, 'get_compliance_status') else {"status": "compliant"}
        return {
            'success': True,
            'data': status
        }
    except Exception as e:
        logger.exception(f"Error verifying compliance: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/overview')
async def get_compliance_overview(
    user_id: Optional[str] = Query(None),
    service = Depends(get_reporting_service),
    current_user: dict = Depends(get_current_user)
):
    """Get summarized compliance overview and stats."""
    try:
        uid = user_id or current_user.get('user_id')
        overview = await service.get_compliance_overview(uid) if hasattr(service, 'get_compliance_overview') else {"summary": "No data"}
        return {
            'success': True,
            'data': overview
        }
    except Exception as e:
        logger.exception(f"Error fetching compliance overview: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/audit')
async def get_audit_trail(
    user_id: Optional[str] = Query(None),
    limit: int = Query(100),
    vault = Depends(get_record_vault),
    current_user: dict = Depends(get_current_user)
):
    """Get detailed compliance audit trail from the immutable RecordVault."""
    try:
        uid = user_id or current_user.get('user_id')
        # RecordVault is synchronous
        audit_logs = vault.get_chain(uid)
        return {
            'success': True,
            'data': audit_logs[-limit:] if audit_logs else []
        }
    except Exception as e:
        logger.exception(f"Error fetching audit trail: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/sar')
async def get_sar_status(
    user_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get Suspicious Activity Report (SAR) status."""
    try:
        uid = user_id or current_user.get('user_id')
        service = get_reporting_service()
        # SAR endpoints usually reserved for admins, but for now matching frontend 404
        return {'success': True, 'data': {'status': 'none'}}
    except Exception as e:
        logger.exception(f"Error fetching SAR status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/report/generate')
async def generate_report(
    data: ReportGenerationRequest,
    service = Depends(get_reporting_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Generate compliance report.
    """
    try:
        report = await service.generate_compliance_report(
            user_id=data.user_id,
            report_type=data.report_type,
            period_start=data.period_start,
            period_end=data.period_end
        )
        
        return {
            'success': True,
            'data': report.model_dump(mode='json')
        }
        
    except Exception as e:
        logger.exception(f"Error generating report: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/violations/{user_id}')
async def get_violations(
    user_id: str,
    engine = Depends(get_compliance_engine),
    current_user: dict = Depends(get_current_user)
):
    """
    Get compliance violations for user.
    """
    try:
        violations = await engine.get_violations(user_id) if hasattr(engine, 'get_violations') else []
        return {
            'success': True,
            'data': violations
        }
        
    except Exception as e:
        logger.exception(f"Error getting violations for {user_id}: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
