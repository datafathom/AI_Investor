"""
Philanthropy API - Endpoints for Impact Investing
Phase 61: Exposes donation routing and ESG analysis features.
"""
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.philanthropy.donation_service import get_donation_service, DonationRecord
from services.analysis.esg_service import get_esg_service, ESGScore, CarbonFootprint

router = APIRouter()

# --- Pydantic Models ---

class DonationRequest(BaseModel):
    amount: float
    allocations: List[Dict[str, float]] # e.g. [{"category": "Climate", "percentage": 40}]

class DonationResponse(BaseModel):
    transaction_id: str
    status: str
    tax_savings: float
    message: str

class ImpactSummary(BaseModel):
    donated_ytd: float
    tax_savings: float
    effective_cost: float

class ESGSummary(BaseModel):
    score: ESGScore
    karma_score: float # 0-100
    sin_stocks: List[Dict]

class CarbonSummary(BaseModel):
    footprint: CarbonFootprint
    scatter_data: List[Dict]

# --- Endpoints ---

@router.post("/donate", response_model=DonationResponse)
async def trigger_donation(request: DonationRequest):
    """Executes a donation routing based on excess alpha."""
    service = get_donation_service()
    try:
        record = await service.route_excess_alpha(request.amount, request.allocations)
        return DonationResponse(
            transaction_id=record.id,
            status=record.status,
            tax_savings=record.tax_savings_est,
            message="Donation routed successfully."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[DonationRecord])
async def get_donation_history():
    """Retrieves past donation records."""
    service = get_donation_service()
    return await service.get_donation_history()

@router.get("/summary", response_model=ImpactSummary)
async def get_impact_summary():
    """Gets YTD impact stats (donations + tax alpha)."""
    service = get_donation_service()
    data = await service.get_tax_impact_summary()
    return ImpactSummary(
        donated_ytd=data["total_donated_ytd"],
        tax_savings=data["estimated_tax_savings"],
        effective_cost=data["effective_cost"]
    )

from services.portfolio_manager import get_portfolio_manager

@router.get("/esg", response_model=ESGSummary)
async def get_esg_metrics():
    """Gets current portfolio ESG scores and alerts."""
    service = get_esg_service()
    pm = get_portfolio_manager()
    
    # Extract tickers from all portfolios
    tickers = [pos.symbol for pos in pm.defensive.positions]
    tickers.extend([pos.symbol for pos in pm.aggressive.positions])
    
    scores = await service.get_portfolio_esg_scores(tickers=tickers)
    sin_stocks = await service.detect_sin_stocks()
    
    # Calculate "Karma Score" (simple agg for now)
    karma = scores.composite * 0.9 # slightly penalized by sin stocks in real logic
    if sin_stocks: karma -= 5 
    
    return ESGSummary(
        score=scores,
        karma_score=round(karma, 1),
        sin_stocks=sin_stocks
    )

@router.get("/carbon", response_model=CarbonSummary)
async def get_carbon_data(portfolio_value: float = Query(3247500.0, description="Current portfolio value")):
    """Gets carbon footprint and scatterplot data."""
    service = get_esg_service()
    pm = get_portfolio_manager()
    
    tickers = [pos.symbol for pos in pm.defensive.positions]
    tickers.extend([pos.symbol for pos in pm.aggressive.positions])
        
    footprint = await service.calculate_carbon_footprint(portfolio_value, tickers=tickers)
    scatter = await service.get_alpha_vs_carbon_data()
    
    return CarbonSummary(
        footprint=footprint,
        scatter_data=scatter
    )
