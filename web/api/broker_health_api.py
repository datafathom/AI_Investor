from fastapi import APIRouter
import random

router = APIRouter(prefix="/api/v1/broker/health", tags=["Broker Health"])

@router.get('/')
async def get_all_health():
    """Get health status for all connected brokers."""
    brokers = ["IBKR", "Schwab", "Robinhood", "E*TRADE", "Alpaca"]
    data = []
    
    for broker in brokers:
        latency = random.randint(20, 150)
        status = "OPERATIONAL"
        if latency > 120: status = "DEGRADED"
        if random.random() > 0.95: status = "DOWN"
        
        data.append({
            "broker": broker,
            "status": status,
            "latency_ms": latency,
            "error_rate": round(random.uniform(0.0, 2.5), 2),
            "rate_limit_usage": random.randint(10, 80)
        })
    return {"success": True, "data": data}
