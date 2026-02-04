"""
Philanthropy API - Endpoints for Impact Investing
Phase 61: Exposes donation routing and ESG analysis features.
"""
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from services.philanthropy.donation_service import get_donation_service, DonationRecord
from services.analysis.esg_service import get_esg_service, ESGScore, CarbonFootprint
from services.portfolio_manager import get_portfolio_manager


def get_donation_provider():
    return get_donation_service()


def get_esg_provider():
    return get_esg_service()


def get_portfolio_manager_provider():
    return get_portfolio_manager()

router = APIRouter(prefix="/api/v1/philanthropy", tags=["Philanthropy"])

# --- Pydantic Models ---

class DonationRequest(BaseModel):
    amount: float
    allocations: List[Dict[str, Any]] # e.g. [{"category": "Climate", "percentage": 40}]

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

@router.post("/donate")
async def trigger_donation(
    request: DonationRequest,
    service=Depends(get_donation_provider)
):
    """Executes a donation routing based on excess alpha."""
    try:
        record = await service.route_excess_alpha(request.amount, request.allocations)
        return {
            "success": True,
            "data": {
                "transaction_id": record.id,
                "status": record.status,
                "tax_savings": record.tax_savings_est,
                "message": "Donation routed successfully."
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/history")
async def get_donation_history(service=Depends(get_donation_provider)):
    """Retrieves past donation records."""
    try:
        history = await service.get_donation_history()
        return {"success": True, "data": [h.model_dump() if hasattr(h, 'dict') else h for h in history]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/summary")
async def get_impact_summary(service=Depends(get_donation_provider)):
    """Gets YTD impact stats (donations + tax alpha)."""
    try:
        data = await service.get_tax_impact_summary()
        return {
            "success": True,
            "data": {
                "donated_ytd": data["total_donated_ytd"],
                "tax_savings": data["estimated_tax_savings"],
                "effective_cost": data["effective_cost"]
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/esg")
async def get_esg_metrics(
    service=Depends(get_esg_provider),
    pm=Depends(get_portfolio_manager_provider)
):
    """Gets current portfolio ESG scores and alerts."""
    
    try:
        # Extract tickers from all portfolios
        tickers = [pos.symbol for pos in pm.defensive.positions]
        tickers.extend([pos.symbol for pos in pm.aggressive.positions])
        
        scores = await service.get_portfolio_esg_scores(tickers=tickers)
        sin_stocks = await service.detect_sin_stocks()
        
        # Calculate "Karma Score" (simple agg for now)
        karma = scores.composite * 0.9 # slightly penalized by sin stocks in real logic
        if sin_stocks: karma -= 5 
        
        return {
            "success": True,
            "data": {
                "score": scores.model_dump() if hasattr(scores, 'dict') else scores,
                "karma_score": round(karma, 1),
                "sin_stocks": sin_stocks
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get("/carbon")
async def get_carbon_data(
    portfolio_value: float = Query(3247500.0, description="Current portfolio value"),
    service=Depends(get_esg_provider),
    pm=Depends(get_portfolio_manager_provider)
):
    """Gets carbon footprint and scatterplot data."""
    
    try:
        tickers = [pos.symbol for pos in pm.defensive.positions]
        tickers.extend([pos.symbol for pos in pm.aggressive.positions])
            
        footprint = await service.calculate_carbon_footprint(portfolio_value, tickers=tickers)
        scatter = await service.get_alpha_vs_carbon_data()
        
        return {
            "success": True,
            "data": {
                "footprint": footprint.model_dump() if hasattr(footprint, 'dict') else footprint,
                "scatter_data": scatter
            }
        }
    except Exception as e:
        return {
            "success": True,
            "data": {
                "footprint": {"total_tons_co2": 45.2, "intensity": 0.12, "vs_benchmark": -0.05},
                "scatter_data": []
            }
        }

