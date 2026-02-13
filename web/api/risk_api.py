from fastapi import APIRouter
import random
from typing import List, Dict

router = APIRouter(prefix="/api/v1/risk", tags=["Risk Management"])

@router.get('/summary')
async def get_risk_summary():
    """Get portfolio-wide risk metrics."""
    return {"success": True, "data": {
        "var_95": -12500.00,
        "var_99": -18000.00,
        "expected_shortfall": -22000.00,
        "beta": 1.15,
        "sharpe": 1.8,
        "current_drawdown": -4.2
    }}

@router.get('/exposures')
async def get_exposures():
    """Get risk exposures by category."""
    return {"success": True, "data": {
        "sector": {"Tech": 45, "Finance": 20, "Healthcare": 15, "Energy": 10, "Other": 10},
        "asset_class": {"Equity": 70, "Options": 20, "Crypto": 5, "Cash": 5}
    }}

@router.post('/sizing/calculate')
async def calculate_position_size(capital: float, risk_per_trade_pct: float, stop_loss_pct: float):
    """Calculate recommended position size using multiple models."""
    risk_amount = capital * (risk_per_trade_pct / 100)
    
    # Fixed Fractional
    fixed_shares = int(risk_amount / (100 * (stop_loss_pct / 100))) # Assuming price 100 for example
    
    # Kelly Criterion (Mock)
    kelly_pct = 0.15 
    kelly_size = capital * kelly_pct

    return {"success": True, "data": {
        "fixed_fractional": {"size": risk_amount * (100/stop_loss_pct), "shares": fixed_shares},
        "kelly_criterion": {"size": kelly_size, "optimal_f": kelly_pct},
        "recommendation": "Use 50% Kelly for stability."
    }}

@router.get('/correlations')
async def get_correlations():
    """Get holdling correlation matrix."""
    symbols = ["AAPL", "MSFT", "GOOG", "TSLA", "SPY"]
    matrix = []
    for s1 in symbols:
        row = {}
        for s2 in symbols:
            if s1 == s2: val = 1.0
            else: val = round(random.uniform(0.3, 0.9), 2)
            row[s2] = val
        matrix.append({"symbol": s1, "correlations": row})
    
    return {"success": True, "data": matrix}
