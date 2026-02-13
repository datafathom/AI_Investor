from fastapi import APIRouter
import uuid
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/alerts", tags=["Alerts"])

class Alert(BaseModel):
    symbol: str
    condition: str
    value: float
    message: Optional[str] = None

@router.get('/')
async def get_active_alerts():
    """Get all active alerts."""
    return {"success": True, "data": [
        {"id": "al_01", "symbol": "NVDA", "condition": "ABOVE", "value": 1200.0, "status": "ACTIVE"},
        {"id": "al_02", "symbol": "SPY", "condition": "BELOW_RSI_30", "value": 30.0, "status": "TRIGGERED"}
    ]}

@router.post('/')
async def create_alert(alert: Alert):
    """Create a new alert."""
    return {"success": True, "data": {"id": str(uuid.uuid4()), "status": "CREATED"}}
