from fastapi import APIRouter
import uuid

router = APIRouter(prefix="/api/v1/watchlist/share", tags=["Watchlist Share"])

@router.post('/{id}')
async def share_watchlist(id: str, email: str):
    """Share a watchlist with a user."""
    return {"success": True, "data": {"token": str(uuid.uuid4()), "permissions": "VIEW"}}

@router.get('/{token}')
async def get_shared_watchlist(token: str):
    """Get a shared watchlist by token."""
    return {"success": True, "data": {
        "name": "Shared: Top Picks 2025",
        "symbols": ["AMZN", "GOOG", "META"],
        "owner": "analyst@fund.com"
    }}
