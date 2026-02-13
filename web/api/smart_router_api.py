"""
Smart Order Router API
Manages routing logic, venue statistics, and best execution compliance.
"""
from fastapi import APIRouter
import random

router = APIRouter(prefix="/api/v1/execution/routing", tags=["Smart Router"])

@router.get("/stats")
async def get_routing_stats():
    venues = ["IEX", "NYSE", "NASDAQ", "MEMX", "DARKPOOLS"]
    stats = []
    
    for venue in venues:
        stats.append({
            "venue": venue,
            "fill_rate": round(random.uniform(0.85, 0.99), 2),
            "avg_latency_ms": random.randint(1, 15),
            "reversion_ms": random.randint(-5, 5),
            "cost_basis_bps": random.randint(5, 30)
        })
        
    return {"success": True, "data": stats}

@router.get("/rules")
async def get_routing_rules():
    return {
        "success": True,
        "data": [
            {"id": 1, "name": "Dark Pool Aggression", "enabled": True, "condition": "Spread > 0.05"},
            {"id": 2, "name": "Lit Market Sweep", "enabled": False, "condition": "Urgency == HIGH"},
            {"id": 3, "name": "Midpoint Peg", "enabled": True, "condition": "Passive && Spread > 0.01"}
        ]
    }
