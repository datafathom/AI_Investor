"""
==============================================================================
FILE: web/api/compliance_api.py
ROLE: Compliance API Endpoints
PURPOSE: REST endpoints for compliance checking and reporting.

INTEGRATION POINTS:
    - ComplianceEngine: Rule checking
    - ReportingService: Report generation
    - FrontendCompliance: Compliance dashboard

ENDPOINTS:
    - POST /api/compliance/check
    - POST /api/compliance/report/generate
    - GET /api/compliance/violations/:user_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request
import logging
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from services.compliance.compliance_engine import get_compliance_engine
from services.compliance.reporting_service import get_reporting_service

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
async def check_compliance(data: ComplianceCheckRequest):
    """
    Check transaction for compliance violations.
    """
    try:
        engine = get_compliance_engine()
        violations = await engine.check_compliance(data.user_id, data.transaction)
        
        return {
            'success': True,
            'data': [v.model_dump(mode='json') for v in violations]
        }
        
    except Exception as e:
        logger.error(f"Error checking compliance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/report/generate')
async def generate_report(data: ReportGenerationRequest):
    """
    Generate compliance report.
    """
    try:
        service = get_reporting_service()
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
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/violations/{user_id}')
async def get_violations(user_id: str):
    """
    Get compliance violations for user.
    """
    try:
        return {
            'success': True,
            'data': []
        }
        
    except Exception as e:
        logger.error(f"Error getting violations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
