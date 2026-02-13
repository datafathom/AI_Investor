from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/reputation", tags=["Reputation"])

@router.get('/sources')
async def list_sources():
    """List data sources and their reputation."""
    return {"success": True, "data": [
        {"id": "src_01", "name": "AlphaVantage", "type": "Market Data", "trust_score": 95, "error_rate": "0.1%", "status": "TRUSTED"},
        {"id": "src_02", "name": "Twitter API", "type": "Social", "trust_score": 60, "error_rate": "2.5%", "status": "WATCHLIST"},
        {"id": "src_03", "name": "Reddit Scraper", "type": "Social", "trust_score": 40, "error_rate": "5.0%", "status": "UNRELIABLE"}
    ]}

@router.put('/sources/{id}')
async def update_trust_score(id: str, score: int):
    """Update source trust score."""
    return {"success": True, "data": {"status": "UPDATED"}}
