from fastapi import APIRouter
import uuid
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/tax", tags=["Tax Reporting"])

@router.get('/liabilities/estimated')
async def calculate_tax_estimates():
    """Calculate estimated tax liabilities."""
    return {"success": True, "data": {
        "federal_short_term": 15000,
        "federal_long_term": 5000,
        "state_tax": 4500,
        "net_investment_income_tax": 1200,
        "total_estimated": 25700
    }}

@router.get('/lots/harvesting')
async def list_harvesting_opportunities():
    """List tax loss harvesting opportunities."""
    return {"success": True, "data": [
        {"symbol": "TSLA", "loss_amount": 3500, "wash_sale_risk": "LOW"},
        {"symbol": "COIN", "loss_amount": 1200, "wash_sale_risk": "MEDIUM"}
    ]}
