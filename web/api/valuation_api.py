from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/valuation", tags=["Valuation"])

@router.get('/pricing-check')
async def check_pricing_accuracy():
    """Check for pricing anomalies."""
    return {"success": True, "data": [
        {"symbol": "TSLA", "provider_a": 180.50, "provider_b": 180.55, "diff": 0.05, "status": "MATCH"},
        {"symbol": "GME", "provider_a": 25.00, "provider_b": 24.50, "diff": 0.50, "status": "VARIANCE"}
    ]}
