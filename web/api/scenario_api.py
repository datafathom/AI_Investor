"""
Scenario API - Macro Shock Simulation
Phase 60: Endpoints for simulating portfolio impact under extreme macro conditions.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

from services.analysis.scenario_service import (
    ScenarioService,
    MacroShock,
    ScenarioResult,
    get_scenario_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/scenario", tags=["Scenario"])

class SimulateRequest(BaseModel):
    id: str
    equity_drop: float
    bond_drop: float
    gold_change: float

class SimulationResponse(BaseModel):
    impact: Dict
    hedge_sufficiency: float
    recovery: Dict

@router.post("/simulate", response_model=SimulationResponse)
async def simulate_scenario(
    request: SimulateRequest,
    portfolio_id: str = "default",
    service: ScenarioService = Depends(get_scenario_service)
):
    try:
        shock = MacroShock(
            id=request.id,
            name=request.id,
            equity_drop=request.equity_drop,
            bond_drop=request.bond_drop,
            gold_change=request.gold_change
        )
        result = await service.apply_shock(portfolio_id, shock)
        sufficiency = await service.calculate_hedge_sufficiency(portfolio_id, shock)
        
        recovery = await service.project_recovery_timeline(result)
        
        return SimulationResponse(
            impact={
                "portfolio_impact_pct": result.portfolio_impact,
                "new_value": result.new_portfolio_value,
                "net_impact_usd": result.net_impact,
                "hedge_offset": result.hedge_offset
            },
            hedge_sufficiency=sufficiency,
            recovery={
                "days": recovery.recovery_days,
                "path": recovery.recovery_path,
                "worst_case": recovery.worst_case_days
            }
        )
    except Exception as e:
        logger.exception("Error in scenario simulation")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monte-carlo-refined")
async def run_refined_mc(
    scenario_id: str,
    initial_value: float,
    service: ScenarioService = Depends(get_scenario_service)
):
    # Dummy shock for context
    shock = MacroShock(id=scenario_id, name=scenario_id, equity_drop=0, bond_drop=0, gold_change=0)
    return await service.run_refined_monte_carlo(initial_value, shock)

@router.get("/bank-run")
async def simulate_bank_run(
    stress_level: float = 1.0,
    portfolio_id: str = "default",
    service: ScenarioService = Depends(get_scenario_service)
):
    return await service.calculate_liquidity_drain(stress_level)
