from fastapi import APIRouter
import uuid
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/opportunities", tags=["Opportunities"])

@router.get('/')
async def list_opportunities():
    """List investment opportunities."""
    return {"success": True, "data": [
        {"id": "opp_01", "title": "Long AI Infrastructure", "status": "RESEARCHING", "conviction": 8, "thesis": "Data center demand outpacing supply."},
        {"id": "opp_02", "title": "Short Regional Banks", "status": "ACTIVE", "conviction": 6, "thesis": "CRE exposure risks."}
    ]}

@router.post('/')
async def create_opportunity(title: str):
    """Create a new opportunity."""
    return {"success": True, "data": {"id": str(uuid.uuid4()), "status": "NEW"}}
