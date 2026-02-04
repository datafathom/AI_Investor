"""
==============================================================================
FILE: web/api/fixed_income_api.py
ROLE: Fixed Income API Endpoints (FastAPI)
PURPOSE: REST endpoints for bond analytics and yield curve.
==============================================================================
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/fixed-income", tags=["Fixed Income"])


class RateShockRequest(BaseModel):
    portfolio_id: str = "default"
    basis_points: int = 100


class DurationRequest(BaseModel):
    par_value: float = 1000
    coupon_rate: float = 0.05
    maturity_years: int = 5
    ytm: float = 0.05


class WALRequest(BaseModel):
    bonds: List[dict] = []


# Mock yield curve data
MOCK_YIELD_CURVE = {
    "date": "2026-02-03",
    "rates": {
        "1M": 5.25, "3M": 5.30, "6M": 5.28, "1Y": 5.15,
        "2Y": 4.85, "3Y": 4.65, "5Y": 4.45, "7Y": 4.35,
        "10Y": 4.28, "20Y": 4.55, "30Y": 4.45
    },
    "is_inverted": True
}


@router.get("/yield-curve")
async def get_yield_curve():
    """Get current Treasury yield curve."""
    return {
        "success": True,
        "data": MOCK_YIELD_CURVE
    }


@router.get("/yield-curve/history")
async def get_yield_curve_history(months: int = Query(12)):
    """Get historical yield curves for animation."""
    # Return mock historical data
    return {
        "success": True,
        "data": [MOCK_YIELD_CURVE]  # Would have multiple curves in production
    }


@router.get("/historical-curves")
async def get_historical_curves(months: int = Query(12)):
    """Get historical yield curves (alias)."""
    return await get_yield_curve_history(months)


@router.post("/rate-shock")
async def simulate_rate_shock(request: RateShockRequest):
    """Simulate rate shock impact on portfolio."""
    # Mock calculation
    value_before = 100000
    pct_change = -0.08 * (request.basis_points / 100)
    value_after = value_before * (1 + pct_change)
    
    return {
        "success": True,
        "data": {
            "shock_basis_points": request.basis_points,
            "portfolio_value_before": value_before,
            "portfolio_value_after": round(value_after, 2),
            "dollar_change": round(value_after - value_before, 2),
            "percentage_change": round(pct_change * 100, 2)
        }
    }


@router.post("/duration")
async def calculate_duration(request: DurationRequest):
    """Calculate duration metrics for a bond."""
    # Simplified Macaulay duration calculation
    mac_duration = request.maturity_years * 0.9  # Simplified
    mod_duration = mac_duration / (1 + request.ytm)
    
    return {
        "success": True,
        "data": {
            "macaulay_duration": round(mac_duration, 2),
            "modified_duration": round(mod_duration, 2),
            "convexity": round(mac_duration * 1.1, 2),
            "dollar_duration": round(request.par_value * mod_duration / 100, 2)
        }
    }


@router.post("/wal")
async def calculate_wal(request: WALRequest):
    """Calculate Weighted Average Life for a bond ladder."""
    if not request.bonds:
        return {
            "success": True,
            "data": {"weighted_average_life": 0, "bond_count": 0}
        }
    
    total_par = sum(b.get("par_value", 1000) for b in request.bonds)
    wal = sum(
        b.get("par_value", 1000) * b.get("maturity_years", 5) 
        for b in request.bonds
    ) / total_par if total_par > 0 else 0
    
    return {
        "success": True,
        "data": {
            "weighted_average_life": round(wal, 2),
            "bond_count": len(request.bonds)
        }
    }


@router.get("/gaps/{portfolio_id}")
async def get_liquidity_gaps(portfolio_id: str):
    """Get liquidity gap analysis for a bond ladder."""
    return {
        "success": True,
        "data": [
            {"year": 2027, "severity": "low", "recommended_action": "Monitor"},
            {"year": 2028, "severity": "medium", "recommended_action": "Consider reinvestment"},
            {"year": 2030, "severity": "high", "recommended_action": "Plan for maturity"}
        ]
    }


@router.get("/inversion")
async def check_inversion():
    """Check if yield curve is currently inverted."""
    spread = MOCK_YIELD_CURVE["rates"]["10Y"] - MOCK_YIELD_CURVE["rates"]["2Y"]
    is_inverted = spread < 0
    
    return {
        "success": True,
        "data": {
            "is_inverted": is_inverted,
            "spread_10y_2y": round(spread, 2),
            "recession_signal": is_inverted
        }
    }
