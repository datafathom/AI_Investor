from fastapi import APIRouter, HTTPException
from typing import Dict, Optional

from services.pricing.probability_cone import ProbabilityConeService

router = APIRouter(prefix="/api/v1/pricing", tags=["Pricing"])

@router.get("/probability-cone/{ticker}")
async def get_probability_cone(ticker: str, price: float = 150.0, iv: float = 0.2, days: int = 30):
    service = ProbabilityConeService()
    return await service.get_probability_cone(ticker, price, iv, days)

@router.get("/expected-move/{ticker}")
async def get_expected_move(ticker: str, price: float = 150.0, iv: float = 0.2, dte: int = 30):
    service = ProbabilityConeService()
    return await service.get_expected_move(ticker, price, iv, dte)
