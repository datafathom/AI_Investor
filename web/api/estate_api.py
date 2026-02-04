"""
==============================================================================
FILE: web/api/estate_api.py
ROLE: Estate Planning API Endpoints
PURPOSE: REST endpoints for estate planning and inheritance simulation.

INTEGRATION POINTS:
    - EstatePlanningService: Estate plan management
    - InheritanceSimulator: Inheritance projections
    - FrontendEstate: Estate dashboard widgets

ENDPOINTS:
    - POST /api/estate/plan/create
    - GET /api/estate/plan/:user_id
    - PUT /api/estate/plan/:plan_id/beneficiary/:beneficiary_id
    - POST /api/estate/tax/calculate
    - POST /api/estate/inheritance/simulate/:plan_id
    - POST /api/estate/inheritance/compare

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import logging
from typing import List, Optional
from pydantic import BaseModel
from services.estate.estate_planning_service import get_estate_planning_service as _get_estate_planning_service
from services.estate.inheritance_simulator import get_inheritance_simulator as _get_inheritance_simulator

def get_estate_planning_provider():
    return _get_estate_planning_service()

def get_inheritance_simulator_provider():
    return _get_inheritance_simulator()
from schemas.estate import EstateScenario

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/estate", tags=["Estate Planning"])

class CreatePlanRequest(BaseModel):
    user_id: str
    beneficiaries: List[dict]
    trust_accounts: Optional[dict] = None

class UpdateBeneficiaryRequest(BaseModel):
    updates: dict

class TaxCalculationRequest(BaseModel):
    estate_value: float
    exemptions: Optional[float] = None

class SimulationRequest(BaseModel):
    projection_years: Optional[int] = 10

class ComparisonRequest(BaseModel):
    scenarios: List[dict]


@router.post('/plan/create')
async def create_estate_plan(
    data: CreatePlanRequest,
    service = Depends(get_estate_planning_provider)
):
    """
    Create estate plan.
    """
    try:
        plan = await service.create_estate_plan(
            user_id=data.user_id,
            beneficiaries=data.beneficiaries,
            trust_accounts=data.trust_accounts
        )
        
        return {
            'success': True,
            'data': plan.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error creating estate plan: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/plan/{user_id}')
async def get_estate_plan(
    user_id: str,
    service = Depends(get_estate_planning_provider)
):
    """
    Get estate plan for user.
    """
    try:
        plan = await service.get_estate_plan_by_user(user_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail='Estate plan not found')
        
        return {
            'success': True,
            'data': plan.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error getting estate plan: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.put('/plan/{plan_id}/beneficiary/{beneficiary_id}')
async def update_beneficiary(
    plan_id: str,
    beneficiary_id: str,
    data: UpdateBeneficiaryRequest,
    service = Depends(get_estate_planning_provider)
):
    """
    Update beneficiary in estate plan.
    """
    try:
        beneficiary = await service.update_beneficiary(
            plan_id=plan_id,
            beneficiary_id=beneficiary_id,
            updates=data.updates
        )
        
        return {
            'success': True,
            'data': beneficiary.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error updating beneficiary: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/tax/calculate')
async def calculate_estate_tax(
    data: TaxCalculationRequest,
    service = Depends(get_estate_planning_provider)
):
    """
    Calculate estate tax.
    """
    try:
        tax_calc = await service.calculate_estate_tax(
            estate_value=data.estate_value,
            exemptions=data.exemptions
        )
        
        return {
            'success': True,
            'data': tax_calc
        }
        
    except Exception as e:
        logger.error(f"Error calculating estate tax: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/inheritance/simulate/{plan_id}')
async def simulate_inheritance(
    plan_id: str,
    data: SimulationRequest,
    simulator = Depends(get_inheritance_simulator_provider)
):
    """
    Simulate inheritance for estate plan.
    """
    try:
        projections = await simulator.simulate_inheritance(
            plan_id=plan_id,
            projection_years=data.projection_years
        )
        
        return {
            'success': True,
            'data': [p.model_dump() for p in projections]
        }
        
    except Exception as e:
        logger.error(f"Error simulating inheritance: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post('/inheritance/compare')
async def compare_inheritance_scenarios(
    data: ComparisonRequest,
    simulator = Depends(get_inheritance_simulator_provider)
):
    """
    Compare inheritance scenarios.
    """
    try:
        scenarios = [EstateScenario(**s) for s in data.scenarios]
        
        results = await simulator.compare_scenarios(scenarios)
        
        return {
            'success': True,
            'data': {
                name: [p.model_dump() for p in projections]
                for name, projections in results.items()
            }
        }
        
    except Exception as e:
        logger.error(f"Error comparing scenarios: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get('/plan')
async def get_estate_plan_by_query(
    user_id: str,
    service = Depends(get_estate_planning_provider)
):
    """
    Get estate plan for user (query param version).
    """
    try:
        plan = await service.get_estate_plan_by_user(user_id)
        
        if plan:
            return {'success': True, 'data': plan.model_dump()}
        
        # Return mock plan as fallback
        return {
            'success': True,
            'data': {
                'plan_id': 'plan_default',
                'user_id': user_id,
                'beneficiaries': [],
                'total_estate_value': 0,
                'status': 'draft'
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting estate plan: {e}")
        return {
            'success': True,
            'data': {
                'plan_id': 'plan_default',
                'user_id': user_id,
                'beneficiaries': [],
                'total_estate_value': 0,
                'status': 'draft'
            }
        }


@router.get('/beneficiaries')
async def get_beneficiaries(
    user_id: str,
    service = Depends(get_estate_planning_provider)
):
    """
    Get beneficiaries for user's estate plan.
    """
    try:
        beneficiaries = await service.get_beneficiaries(user_id)
        return {'success': True, 'data': [b.model_dump() if hasattr(b, 'model_dump') else b for b in beneficiaries] if beneficiaries else []}
    except Exception as e:
        logger.error(f"Error getting beneficiaries: {e}")
        # Return empty list as fallback
        return {'success': True, 'data': []}

