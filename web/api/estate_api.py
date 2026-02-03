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
import logging
from typing import List, Optional
from pydantic import BaseModel
from services.estate.estate_planning_service import get_estate_planning_service
from services.estate.inheritance_simulator import get_inheritance_simulator
from models.estate import EstateScenario

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
async def create_estate_plan(data: CreatePlanRequest):
    """
    Create estate plan.
    """
    try:
        service = get_estate_planning_service()
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
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/plan/{user_id}')
async def get_estate_plan(user_id: str):
    """
    Get estate plan for user.
    """
    try:
        service = get_estate_planning_service()
        plan = await service.get_estate_plan_by_user(user_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail='Estate plan not found')
        
        return {
            'success': True,
            'data': plan.model_dump()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting estate plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/plan/{plan_id}/beneficiary/{beneficiary_id}')
async def update_beneficiary(plan_id: str, beneficiary_id: str, data: UpdateBeneficiaryRequest):
    """
    Update beneficiary in estate plan.
    """
    try:
        service = get_estate_planning_service()
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
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/tax/calculate')
async def calculate_estate_tax(data: TaxCalculationRequest):
    """
    Calculate estate tax.
    """
    try:
        service = get_estate_planning_service()
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
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/inheritance/simulate/{plan_id}')
async def simulate_inheritance(plan_id: str, data: SimulationRequest):
    """
    Simulate inheritance for estate plan.
    """
    try:
        simulator = get_inheritance_simulator()
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
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/inheritance/compare')
async def compare_inheritance_scenarios(data: ComparisonRequest):
    """
    Compare inheritance scenarios.
    """
    try:
        scenarios = [EstateScenario(**s) for s in data.scenarios]
        
        simulator = get_inheritance_simulator()
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
        raise HTTPException(status_code=500, detail=str(e))
