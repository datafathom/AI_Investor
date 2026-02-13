from fastapi import APIRouter
import uuid
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/wealth", tags=["Wealth Planning"])

@router.get('/estate/map')
async def get_estate_structure_map():
    """Get estate flow diagram data."""
    return {"success": True, "data": {
        "grantor": "John Doe",
        "trusts": [
            {"id": "t_01", "name": "Doe Family Revocable Trust", "type": "Revocable", "assets": 5000000},
            {"id": "t_02", "name": "JD 2024 Irrevocable Trust", "type": "Irrevocable", "assets": 2000000}
        ],
        "beneficiaries": [
            {"id": "b_01", "name": "Jane Doe (Spouse)", "share": 0.5},
            {"id": "b_02", "name": "Little Jimmy (Son)", "share": 0.25},
            {"id": "b_03", "name": "Little Sally (Daughter)", "share": 0.25}
        ]
    }}

@router.get('/beneficiaries')
async def list_beneficiaries():
    """List all beneficiaries."""
    return {"success": True, "data": [
        {"id": "b_01", "name": "Jane Doe", "relationship": "Spouse", "allocation": "50%"},
        {"id": "b_02", "name": "Jimmy Doe", "relationship": "Child", "allocation": "25%"},
        {"id": "b_03", "name": "Sally Doe", "relationship": "Child", "allocation": "25%"}
    ]}

@router.post('/scenarios/run')
async def model_life_event_impact(event_type: str):
    """Model impact of a life event."""
    return {"success": True, "data": {
        "scenario": event_type,
        "impact": "Estate Tax Liability: $1,200,000",
        "liquidity_gap": 0,
        "recommendations": ["Fund ILIT for liquidity", "Review beneficiary designations"]
    }}

@router.get('/gifting/status')
async def get_annual_gift_allowance():
    """Get annual gifting status."""
    return {"success": True, "data": {
        "annual_exclusion": 18000,
        "used": 10000,
        "remaining": 8000,
        "recipients": [
            {"name": "Jimmy Doe", "amount": 5000},
            {"name": "Sally Doe", "amount": 5000}
        ],
        "lifetime_exemption_used": 2500000,
        "lifetime_exemption_total": 13610000
    }}

@router.post('/gifting/record')
async def record_gift_transaction(recipient: str, amount: float):
    """Record a gift transaction."""
    return {"success": True, "data": {"status": "RECORDED", "id": str(uuid.uuid4())}}

@router.get('/trusts/compliance')
async def check_trust_rules():
    """Check trust compliance rules."""
    return {"success": True, "data": [
        {"rule": "HEMS Standard", "status": "COMPLIANCE", "last_check": "2024-05-15"},
        {"rule": "Crummey Notices", "status": "PENDING", "action_needed": "Send 2 notices for 2024 contributions"}
    ]}

@router.get('/trusts/distributions')
async def list_pending_distributions():
    """List pending trust distributions."""
    return {"success": True, "data": [
        {"trust": "Doe Family Revocable Trust", "beneficiary": "Jane Doe", "amount": 15000, "reason": "Monthly Income"}
    ]}

@router.get('/sustainability')
async def calculate_wealth_longevity():
    """Calculate wealth sustainability metrics."""
    return {"success": True, "data": {
        "years_until_exhaustion": "Indefinite (>100)",
        "sustainability_score": 95,
        "legacy_projection": 15000000,
        "burn_rate": 0.035
    }}
