"""
Retirement Planning API - FastAPI Router
REST endpoints for retirement projections and withdrawal strategies.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.retirement.retirement_projection_service import get_retirement_projection_service
from services.retirement.withdrawal_strategy_service import get_withdrawal_strategy_service
from schemas.retirement import RetirementScenario


def get_projection_provider():
    return get_retirement_projection_service()


def get_withdrawal_provider():
    return get_withdrawal_strategy_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/retirement", tags=["Retirement"])

class ProjectRetirementRequest(BaseModel):
    scenario: Dict[str, Any]
    n_simulations: int = 10000

class CompareScenariosRequest(BaseModel):
    scenarios: List[Dict[str, Any]]
    n_simulations: int = 10000

class WithdrawalPlanRequest(BaseModel):
    user_id: str
    strategy: str = 'inflation_adjusted'
    initial_withdrawal_amount: float = 0.0
    withdrawal_rate: Optional[float] = None
    inflation_adjustment: bool = True

class OptimizeWithdrawalRequest(BaseModel):
    retirement_savings: float
    annual_expenses: float
    years_in_retirement: int = 30
    expected_return: float = 0.06

@router.post('/project')
async def project_retirement(
    request_data: ProjectRetirementRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_projection_provider)
):
    """Project retirement with Monte Carlo simulation."""
    try:
        scenario = RetirementScenario(**request_data.scenario)
        projection = await service.project_retirement(scenario, request_data.n_simulations)
        
        return {
            'success': True,
            'data': projection.model_dump()
        }
    except Exception as e:
        logger.error(f"Error projecting retirement: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/compare')
async def compare_scenarios(
    request_data: CompareScenariosRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_projection_provider)
):
    """Compare multiple retirement scenarios."""
    try:
        scenarios = [RetirementScenario(**s) for s in request_data.scenarios]
        results = await service.compare_scenarios(scenarios, request_data.n_simulations)
        
        return {
            'success': True,
            'data': {name: proj.model_dump() for name, proj in results.items()}
        }
    except Exception as e:
        logger.error(f"Error comparing scenarios: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/withdrawal/plan')
async def create_withdrawal_plan(
    request_data: WithdrawalPlanRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_withdrawal_provider)
):
    """Create withdrawal plan."""
    try:
        plan = await service.create_withdrawal_plan(
            user_id=request_data.user_id,
            strategy=request_data.strategy,
            initial_withdrawal_amount=request_data.initial_withdrawal_amount,
            withdrawal_rate=request_data.withdrawal_rate,
            inflation_adjustment=request_data.inflation_adjustment
        )
        
        return {
            'success': True,
            'data': plan.model_dump()
        }
    except Exception as e:
        logger.error(f"Error creating withdrawal plan: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/rmd/{user_id}')
async def get_rmds(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_withdrawal_provider)
):
    """Get RMD calculations for user."""
    try:
        accounts = await service._get_account_balances(user_id)
        rmds = await service._calculate_rmds(user_id, accounts)
        
        return {
            'success': True,
            'data': rmds or {}
        }
    except Exception as e:
        logger.error(f"Error calculating RMDs: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/withdrawal/optimize')
async def optimize_withdrawal_rate(
    request_data: OptimizeWithdrawalRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    service=Depends(get_withdrawal_provider)
):
    """Optimize withdrawal rate."""
    try:
        result = await service.optimize_withdrawal_rate(
            retirement_savings=request_data.retirement_savings,
            annual_expenses=request_data.annual_expenses,
            years_in_retirement=request_data.years_in_retirement,
            expected_return=request_data.expected_return
        )
        
        return {
            'success': True,
            'data': result
        }
    except Exception as e:
        logger.error(f"Error optimizing withdrawal rate: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
