"""
Scanner API - FastAPI Router
Migrated from Flask (web/api/scanner_api.py)
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Optional, Any
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/scanner", tags=["Scanner"])

@router.get("/matches")
async def get_scanner_matches():
    """Returns the latest asset matches based on technical/AI signals."""
    assets = ['NVDA', 'TSLA', 'AAPL', 'AMD', 'PLTR', 'COIN', 'MSFT', 'META', 'GOOGL', 'AMZN']
    sectors = ['TECH', 'CONSUMER', 'TECH', 'DATA', 'FINANCE', 'TECH', 'SOCIAL', 'TECH', 'RETAIL']
    signals = ['BULLISH', 'BEARISH', 'NEUTRAL']
    
    matches = []
    for i in range(10):
        symbol = random.choice(assets)
        matches.append({
            "id": i,
            "asset": symbol,
            "change": round(random.uniform(-5, 5), 2),
            "sector": random.choice(sectors),
            "signal": random.choice(signals),
            "timestamp": datetime.now().isoformat() + "Z"
        })
    
    return {"success": True, "data": matches}

@router.get("/galaxy")
async def get_galaxy_data():
    """Returns 3D correlation data for the Galaxy View."""
    stars = []
    for i in range(100):
        stars.append({
            "id": i,
            "ticker": f"ASSET_{i}",
            "x": round(random.uniform(-400, 400), 2),
            "y": round(random.uniform(-250, 250), 2),
            "z": round(random.uniform(-500, 500), 2),
            "size": round(random.uniform(1, 5), 2),
            "color": "#10b981" if random.random() > 0.5 else "#ef4444"
        })
    return {"success": True, "data": stars}

@router.get("/pulse")
async def get_market_pulse():
    """Returns sector momentum data."""
    sectors = ['Tech', 'Finance', 'Energy', 'Health', 'Retail', 'Defense']
    data = []
    for s in sectors:
        data.append({
            "name": s,
            "change": round(random.uniform(-3, 3), 2)
        })
    return {"success": True, "data": data}
