"""
Advanced Risk Management API - FastAPI Router
REST endpoints for advanced risk metrics and stress testing.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.risk.advanced_risk_metrics_service import get_risk_metrics_service
from services.risk.stress_testing_service import get_stress_testing_service
from schemas.risk import StressScenario

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/risk", tags=["Risk Management"])
# Alias for advanced frontend services
router_advanced = APIRouter(prefix="/api/v1/advanced-risk", tags=["Advanced Risk"])

class HistoricalStressRequest(BaseModel):
    scenario_name: str

class MonteCarloStressRequest(BaseModel):
    n_simulations: int = 10000
    time_horizon_days: int = 252

class CustomStressRequest(BaseModel):
    scenario: StressScenario

@router.get('/metrics/{portfolio_id}')
@router_advanced.get('/risk-metrics')
async def get_risk_metrics(
    portfolio_id: Optional[str] = None,
    method: str = 'historical',
    lookback_days: int = 252,
    service = Depends(get_risk_metrics_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get comprehensive risk metrics for portfolio.
    Supports both /risk/metrics/{id} and /advanced-risk/risk-metrics?portfolio_id=...
    """
    try:
        pid = portfolio_id or "default-portfolio"
        metrics = await service.calculate_risk_metrics(
            portfolio_id=pid,
            method=method,
            lookback_days=lookback_days
        )
        
        return {
            'success': True,
            'data': metrics.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/stress/historical/{portfolio_id}')
async def run_historical_stress(
    portfolio_id: str,
    request_data: HistoricalStressRequest,
    service = Depends(get_stress_testing_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Run historical scenario stress test.
    """
    try:
        result = await service.run_historical_scenario(
            portfolio_id=portfolio_id,
            scenario_name=request_data.scenario_name
        )
        
        return {
            'success': True,
            'data': result.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error running historical stress test: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/stress/monte_carlo/{portfolio_id}')
async def run_monte_carlo_stress(
    portfolio_id: str,
    request_data: MonteCarloStressRequest,
    service = Depends(get_stress_testing_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Run Monte Carlo stress test.
    """
    try:
        result = await service.run_monte_carlo_simulation(
            portfolio_id=portfolio_id,
            n_simulations=request_data.n_simulations,
            time_horizon_days=request_data.time_horizon_days
        )
        
        return {
            'success': True,
            'data': result.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error running Monte Carlo stress test: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/stress/custom/{portfolio_id}')
async def run_custom_stress(
    portfolio_id: str,
    request_data: CustomStressRequest,
    service = Depends(get_stress_testing_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Run custom stress scenario.
    """
    try:
        result = await service.run_custom_stress_scenario(
            portfolio_id=portfolio_id,
            scenario=request_data.scenario
        )
        
        return {
            'success': True,
            'data': result.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error running custom stress test: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
