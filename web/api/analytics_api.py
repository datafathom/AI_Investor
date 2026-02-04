"""
Analytics API - FastAPI Router
REST endpoints for portfolio analytics including performance 
attribution and risk decomposition.
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.analytics.performance_attribution_service import get_attribution_service
from services.analytics.risk_decomposition_service import get_risk_decomposition_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get('/attribution/{portfolio_id}')
@router.get('/performance-attribution')
async def get_performance_attribution(
    portfolio_id: Optional[str] = None,
    start_date: str = '2024-01-01',
    end_date: Optional[str] = None,
    benchmark: Optional[str] = None,
    attribution_type: str = 'multi_factor',
    service = Depends(get_attribution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get performance attribution for a portfolio.
    Supports both path param (Legacy/Standard) and query param (analyticsService.js).
    """
    try:
        # Use provided ID or default
        pid = portfolio_id or "default-portfolio"
        
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        attribution = await service.calculate_attribution(
            portfolio_id=pid,
            start_date=start_dt,
            end_date=end_dt,
            benchmark=benchmark,
            attribution_type=attribution_type
        )
        
        return {
            'success': True,
            'data': attribution.model_dump()
        }
    except Exception as e:
        logger.error(f"Error calculating attribution: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/risk-decomposition')
async def get_risk_decomposition(
    portfolio_id: Optional[str] = None,
    factor_model: str = 'fama_french',
    lookback_days: int = 252,
    service = Depends(get_risk_decomposition_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get factor risk decomposition.
    Specifically requested by AdvancedPortfolioAnalytics.jsx
    """
    try:
        pid = portfolio_id or "default-portfolio"
        risk_analysis = await service.decompose_factor_risk(
            portfolio_id=pid,
            factor_model=factor_model,
            lookback_days=lookback_days
        )
        return {
            'success': True,
            'data': risk_analysis.model_dump()
        }
    except Exception as e:
        logger.error(f"Error calculating risk decomposition: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/contribution/{portfolio_id}')
async def get_contribution(
    portfolio_id: str,
    start_date: str = '2024-01-01',
    end_date: Optional[str] = None,
    service = Depends(get_attribution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get holding contribution analysis.
    """
    try:
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        contributions = await service.calculate_holding_contributions(
            portfolio_id=portfolio_id,
            start_date=start_dt,
            end_date=end_dt
        )
        
        return {
            'success': True,
            'data': [c.model_dump() for c in contributions]
        }
    except Exception as e:
        logger.error(f"Error calculating contribution: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/risk/factor/{portfolio_id}')
async def get_factor_risk(
    portfolio_id: str,
    factor_model: str = 'fama_french',
    lookback_days: int = 252,
    service = Depends(get_risk_decomposition_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get factor risk decomposition for a portfolio."""
    try:
        risk_analysis = await service.decompose_factor_risk(
            portfolio_id=portfolio_id,
            factor_model=factor_model,
            lookback_days=lookback_days
        )
        
        return {
            'success': True,
            'data': risk_analysis.model_dump()
        }
    except Exception as e:
        logger.error(f"Error calculating factor risk: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/risk/concentration/{portfolio_id}')
async def get_concentration_risk(
    portfolio_id: str,
    dimensions: str = 'holding,sector,geography',
    service = Depends(get_risk_decomposition_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get concentration risk analysis for a portfolio."""
    try:
        dim_list = [d.strip() for d in dimensions.split(',')]
        concentration = await service.calculate_concentration_risk(
            portfolio_id=portfolio_id,
            dimensions=dim_list
        )
        
        return {
            'success': True,
            'data': concentration.model_dump()
        }
    except Exception as e:
        logger.error(f"Error calculating concentration risk: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/risk/correlation/{portfolio_id}')
async def get_correlation(
    portfolio_id: str,
    lookback_days: int = 252,
    service = Depends(get_risk_decomposition_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get correlation analysis for a portfolio."""
    try:
        correlation = await service.analyze_correlation(
            portfolio_id=portfolio_id,
            lookback_days=lookback_days
        )
        
        return {
            'success': True,
            'data': correlation.model_dump()
        }
    except Exception as e:
        logger.error(f"Error calculating correlation: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/risk/tail/{portfolio_id}')
async def get_tail_risk(
    portfolio_id: str,
    confidence_level: float = 0.95,
    method: str = 'historical',
    service = Depends(get_risk_decomposition_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get tail risk contributions for a portfolio."""
    try:
        tail_risk = await service.calculate_tail_risk_contributions(
            portfolio_id=portfolio_id,
            confidence_level=confidence_level,
            method=method
        )
        
        return {
            'success': True,
            'data': tail_risk.model_dump()
        }
    except Exception as e:
        logger.error(f"Error calculating tail risk: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
