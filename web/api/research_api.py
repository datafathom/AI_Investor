"""
==============================================================================
FILE: web/api/research_api.py
ROLE: Research & Reports API Endpoints (FastAPI)
PURPOSE: REST endpoints for research report generation and download.
==============================================================================
"""

import logging
from fastapi import APIRouter, HTTPException, Depends, Request, Query, Response
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.research.research_service import get_research_service
from services.research.report_generator import get_report_generator
from web.auth_utils import get_current_user


def get_research_provider():
    return get_research_service()


def get_report_generator_provider():
    return get_report_generator()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/research", tags=["Research"])

class PortfolioReportRequest(BaseModel):
    user_id: str
    portfolio_id: str
    title: Optional[str] = None

class CompanyResearchRequest(BaseModel):
    user_id: str
    symbol: str
    title: Optional[str] = None

class ReportGenerateRequest(BaseModel):
    user_id: Optional[str] = 'default_user'
    template_id: str
    report_title: Optional[str] = None


@router.post('/portfolio-report')
async def generate_portfolio_report(
    data: PortfolioReportRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_research_provider)
):
    """
    Generate portfolio analysis report.
    """
    try:
        report = await service.generate_portfolio_report(
            user_id=data.user_id,
            portfolio_id=data.portfolio_id,
            title=data.title
        )
        return {'success': True, 'data': report.model_dump()}
    except Exception as e:
        logger.exception(f"Error generating portfolio report: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/company-research')
async def generate_company_research(
    data: CompanyResearchRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_research_provider)
):
    """
    Generate company research report.
    """
    try:
        report = await service.generate_company_research(
            user_id=data.user_id,
            symbol=data.symbol,
            title=data.title
        )
        return {'success': True, 'data': report.model_dump()}
    except Exception as e:
        logger.exception(f"Error generating company research: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/reports')
async def get_user_reports(
    user_id: str = Query('default_user'),
    current_user: dict = Depends(get_current_user),
    service=Depends(get_research_provider)
):
    """
    Get all reports for a user.
    """
    try:
        reports = await service._get_reports_from_db(user_id)
        return {'success': True, 'data': [r.model_dump() for r in reports]}
    except Exception as e:
        logger.exception(f"Error getting reports for {user_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/templates')
async def get_templates(current_user: dict = Depends(get_current_user)):
    """
    Get available report templates.
    """
    return {
        'success': True,
        'data': [
            {"template_id": "equity_deep_dive", "template_name": "Equity Deep Dive", "description": "Fundamental analysis for stocks.", "category": "Equities"},
            {"template_id": "macro_regime_shift", "template_name": "Macro Regime Shift", "description": "Analysis of regime changes.", "category": "Macro"},
            {"template_id": "risk_contagion", "template_name": "Risk Contagion", "description": "Network-based risk propagation.", "category": "Risk"}
        ]
    }


@router.post('/generate')
async def generate_report_generic(
    data: ReportGenerateRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_research_provider)
):
    """
    Generate a new report based on template.
    """
    try:
        # Mapping all templates to SPY for demo purposes as in original code
        report = await service.generate_company_research(
            user_id=data.user_id,
            symbol="SPY",
            title=data.report_title
        )
        return {'success': True, 'data': report.model_dump()}
    except Exception as e:
        logger.exception(f"Error generating report: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/report/{report_id}/pdf')
async def download_pdf(
    report_id: str,
    current_user: dict = Depends(get_current_user),
    generator=Depends(get_report_generator_provider)
):
    """Download report as PDF."""
    try:
        pdf_bytes = await generator.generate_pdf(report_id)
        return Response(
            pdf_bytes, 
            media_type='application/pdf', 
            headers={'Content-Disposition': f'attachment; filename=report_{report_id}.pdf'}
        )
    except Exception as e:
        logger.exception(f"Error generating PDF for {report_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/report/{report_id}/html')
async def download_html(
    report_id: str,
    current_user: dict = Depends(get_current_user),
    generator=Depends(get_report_generator_provider)
):
    """Download report as HTML."""
    try:
        html = await generator.generate_html(report_id)
        return Response(
            html, 
            media_type='text/html', 
            headers={'Content-Disposition': f'attachment; filename=report_{report_id}.html'}
        )
    except Exception as e:
        logger.exception(f"Error generating HTML for {report_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/report/{report_id}/excel')
async def download_excel(
    report_id: str,
    current_user: dict = Depends(get_current_user),
    generator=Depends(get_report_generator_provider)
):
    """Download report as Excel."""
    try:
        excel_bytes = await generator.generate_excel(report_id)
        return Response(
            excel_bytes, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            headers={'Content-Disposition': f'attachment; filename=report_{report_id}.xlsx'}
        )
    except Exception as e:
        logger.exception(f"Error generating Excel for {report_id}: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
