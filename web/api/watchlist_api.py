from fastapi import APIRouter
import uuid
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/watchlist", tags=["Watchlist"])

class Watchlist(BaseModel):
    id: str
    name: str
    symbols: List[str]
    tags: List[str] = []

@router.get('/')
async def list_watchlists():
    """List all user watchlists."""
    return {"success": True, "data": [
        {"id": "wl_01", "name": "Tech Giants", "symbols": ["AAPL", "MSFT", "GOOGL"], "tags": ["Growth", "Long-Term"]},
        {"id": "wl_02", "name": "Crypto Plays", "symbols": ["COIN", "MSTR", "MARA"], "tags": ["High Volatility"]},
        {"id": "wl_03", "name": "Dividend Kings", "symbols": ["KO", "PG", "JNJ"], "tags": ["Income"]}
    ]}

@router.post('/')
async def create_watchlist(name: str):
    """Create a new watchlist."""
    return {"success": True, "data": {"id": str(uuid.uuid4()), "name": name, "symbols": []}}

@router.put('/{id}/symbols')
async def update_symbols(id: str, symbols: List[str]):
    """Update symbols in a watchlist."""
    return {"success": True, "data": {"id": id, "count": len(symbols)}}
