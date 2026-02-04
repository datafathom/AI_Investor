"""
Attribution API - FastAPI Router
REST endpoints for portfolio performance attribution.
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.analysis.attribution_service import (
    AttributionService,
    DateRange
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/attribution", tags=["Attribution"])

# Singleton service instance
_service = AttributionService()

def get_attribution_service():
    """Dependency for getting the attribution service."""
    return _service

class AttributionPeriod(BaseModel):
    start: str
    end: str

class BenchmarkComparisonRequest(BaseModel):
    portfolio_id: str
    benchmarks: List[str] = ['sp500', 'nasdaq']
    period: AttributionPeriod = AttributionPeriod(start='2025-01-01', end='2025-12-31')

# CRITICAL: Static routes MUST come before dynamic routes
@router.get('/benchmarks')
async def get_benchmarks(
    service = Depends(get_attribution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get list of available benchmarks for attribution comparison."""
    benchmarks = service.get_available_benchmarks()
    return {
        "success": True,
        "data": benchmarks
    }

@router.post('/compare')
async def compare_benchmarks(
    request_data: BenchmarkComparisonRequest,
    service = Depends(get_attribution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Compare portfolio attribution against multiple benchmarks."""
    try:
        portfolio_id = request_data.portfolio_id
        benchmark_ids = request_data.benchmarks
        period = DateRange(start=request_data.period.start, end=request_data.period.end)
        
        results = []
        for benchmark_id in benchmark_ids:
            result = await service.calculate_brinson_attribution(
                portfolio_id=portfolio_id,
                benchmark_id=benchmark_id,
                period=period
            )
            results.append({
                "benchmark_id": benchmark_id,
                "total_active_return": result.total_active_return,
                "total_allocation_effect": result.total_allocation_effect,
                "total_selection_effect": result.total_selection_effect,
                "total_interaction_effect": result.total_interaction_effect
            })
        
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        logger.error(f"Benchmark comparison failed: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/sector/{portfolio_id}/{sector}')
async def get_sector_attribution(
    portfolio_id: str,
    sector: str,
    service = Depends(get_attribution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get attribution for a specific sector."""
    try:
        allocation = await service.get_sector_allocation_effect(portfolio_id, sector)
        selection = await service.get_selection_effect(portfolio_id, sector)
        
        return {
            "success": True,
            "data": {
                "sector": sector,
                "allocation_effect": allocation,
                "selection_effect": selection
            }
        }
    except Exception as e:
        logger.error(f"Sector attribution failed: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/{portfolio_id}')
async def get_attribution(
    portfolio_id: str,
    benchmark: str = 'sp500',
    start: str = '2025-01-01',
    end: str = '2025-12-31',
    service = Depends(get_attribution_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get full Brinson-Fachler attribution for a portfolio."""
    try:
        result = await service.calculate_brinson_attribution(
            portfolio_id=portfolio_id,
            benchmark_id=benchmark,
            period=DateRange(start=start, end=end)
        )
        
        return {
            "success": True,
            "data": {
                "portfolio_id": result.portfolio_id,
                "benchmark_id": result.benchmark_id,
                "period": {
                    "start": result.period.start,
                    "end": result.period.end
                },
                "total_active_return": result.total_active_return,
                "total_allocation_effect": result.total_allocation_effect,
                "total_selection_effect": result.total_selection_effect,
                "total_interaction_effect": result.total_interaction_effect,
                "sector_attributions": [
                    {
                        "sector": sa.sector,
                        "allocation_effect": sa.allocation_effect,
                        "selection_effect": sa.selection_effect,
                        "interaction_effect": sa.interaction_effect,
                        "portfolio_weight": sa.portfolio_weight,
                        "benchmark_weight": sa.benchmark_weight,
                        "portfolio_return": sa.portfolio_return,
                        "benchmark_return": sa.benchmark_return
                    }
                    for sa in result.sector_attributions
                ],
                "regime_shifts": [
                    {
                        "start_date": rs.start_date,
                        "end_date": rs.end_date,
                        "correlation_before": rs.correlation_before,
                        "correlation_during": rs.correlation_during,
                        "impact_basis_points": rs.impact_basis_points,
                        "description": rs.description
                    }
                    for rs in result.regime_shifts
                ],
                "calculated_at": result.calculated_at
            }
        }
    except Exception as e:
        logger.error(f"Attribution calculation failed: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
