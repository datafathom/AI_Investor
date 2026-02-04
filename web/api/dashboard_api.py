"""
==============================================================================
FILE: web/api/dashboard_api.py
ROLE: Mission Control Data Feed (FastAPI)
PURPOSE: Expose Strategy, Risk, and Execution status to the Frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
import logging
from typing import Optional, Dict, Any

from services.strategy.dynamic_allocator import get_dynamic_allocator
from services.risk.risk_monitor import get_risk_monitor
from services.risk.circuit_breaker import get_circuit_breaker
from services.execution.paper_exchange import get_paper_exchange

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


# TODO: Replace with real auth dependency
async def login_required():
    pass


@router.get("/allocation", dependencies=[Depends(login_required)])
async def get_allocation(
    fear_index: float = Query(50.0),
    allocator = Depends(get_dynamic_allocator)
):
    """Get current target allocation based on Fear Index."""
    try:
        # High Level Buckets
        buckets = allocator.allocate_capital(fear_index)
        
        # Detailed Portfolio (Mock Assets for now)
        import pandas as pd
        mock_assets = {
            'SPY': pd.DataFrame({'close': [400.0]}),
            'TLT': pd.DataFrame({'close': [100.0]})
        }
        targets = allocator.construct_target_portfolio(mock_assets, fear_index)
        
        return {
            "success": True,
            "data": {
                "fear_index": fear_index,
                "buckets": buckets,
                "target_weights": targets
            }
        }
    except Exception as e:
        logger.exception("Failed to fetch allocation")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/risk", dependencies=[Depends(login_required)])
async def get_risk_status(
    monitor = Depends(get_risk_monitor),
    breaker = Depends(get_circuit_breaker),
    exchange = Depends(get_paper_exchange)
):
    """Retrieve real-time Risk Metrics and Circuit Breaker status."""
    try:
        # Mock Portfolio for VaR
        summary = exchange.get_account_summary()
        cash = summary['cash']
        
        # Calculate VaR
        var_95 = monitor.calculate_parametric_var(cash, 0.02)
        
        return {
            "success": True,
            "data": {
                "var_95_daily": var_95,
                "portfolio_frozen": breaker.portfolio_frozen,
                "freeze_reason": breaker.freeze_reason,
                "frozen_assets": list(breaker.frozen_assets)
            }
        }
    except Exception as e:
        logger.exception("Failed to fetch risk status")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/execution", dependencies=[Depends(login_required)])
async def get_execution_status(exchange = Depends(get_paper_exchange)):
    """Fetch Paper Trading Account balance and current positions."""
    try:
        summary = exchange.get_account_summary()
        
        return {
            "success": True,
            "data": {
                "balance": summary["cash"],
                "positions": summary["positions"]
            }
        }
    except Exception as e:
        logger.exception("Failed to fetch execution status")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
