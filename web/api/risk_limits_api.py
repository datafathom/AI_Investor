from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/risk/limits", tags=["Risk Limits"])

class RiskLimit(BaseModel):
    id: str
    name: str
    limit_type: str
    value: float
    action: str

@router.get('/')
async def get_risk_limits():
    """Get active risk limits."""
    return {"success": True, "data": [
        {"id": "rl_01", "name": "Max Drawdown Stop", "limit_type": "DRAWDOWN", "value": 10.0, "action": "HALT_TRADING"},
        {"id": "rl_02", "name": "Single Pos Size", "limit_type": "CONCENTRATION", "value": 20.0, "action": "REJECT_ORDER"},
        {"id": "rl_03", "name": "Gross Exposure", "limit_type": "LEVERAGE", "value": 200.0, "action": "WARNING"}
    ]}
