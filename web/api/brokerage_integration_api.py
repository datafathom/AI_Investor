from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/brokerage/integration", tags=["Broker Integration"])

@router.get('/compare')
async def compare_brokers():
    """Compare broker fees and features."""
    return {"success": True, "data": [
        {
            "broker": "IBKR",
            "fees": {"stock": 0.005, "option": 0.65, "margin_rate": 6.8},
            "features": ["API", "Algos", "Global Access"],
            "rating": 4.8
        },
        {
            "broker": "Schwab",
            "fees": {"stock": 0.0, "option": 0.65, "margin_rate": 11.5},
            "features": ["Research", "Banking", "Support"],
            "rating": 4.5
        },
        {
            "broker": "Robinhood",
            "fees": {"stock": 0.0, "option": 0.0, "margin_rate": 8.0},
            "features": ["Mobile UI", "Crypto", "Cash Sweeps"],
            "rating": 4.0
        }
    ]}
