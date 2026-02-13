from fastapi import APIRouter
import uuid

router = APIRouter(prefix="/api/v1/screener", tags=["Screener"])

@router.post('/run')
async def run_screen():
    """Run a stock screen."""
    return {"success": True, "data": [
        {"symbol": "AMD", "price": 165.50, "change_pct": 3.2, "volume": 50000000},
        {"symbol": "TSLA", "price": 180.20, "change_pct": -1.5, "volume": 80000000}
    ]}

@router.get('/saved')
async def list_saved_screens():
    """List saved screen criteria."""
    return {"success": True, "data": [
        {"id": "scr_01", "name": "High Growth Tech", "criteria": "Rev Growth > 20% AND P/S < 10"},
        {"id": "scr_02", "name": "Oversold Blue Chips", "criteria": "RSI < 30 AND Mkt Cap > 100B"}
    ]}
