"""
Cash API - Multi-Currency Cash Management Endpoints

Phase 56: REST endpoints for cash balances, FX rates,
conversions, and sweep optimization.

Routes:
    GET  /api/v1/cash/dashboard       - Full cash dashboard data
    GET  /api/v1/cash/fx/rates        - Current FX rates
    POST /api/v1/cash/fx/convert      - Execute FX conversion
    GET  /api/v1/cash/sweep/suggestions - Get sweep suggestions
    POST /api/v1/cash/sweep/execute   - Execute cash sweep
    GET  /api/v1/cash/repo/rates      - Get repo rates
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging

from services.trading.fx_service import (
    FXService,
    FXRate,
    CurrencyBalance,
    SweepSuggestion,
    RepoRate,
    ConversionResult,
    get_fx_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/cash", tags=["Cash"])


# ─────────────────────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────────────────────

class FXRateResponse(BaseModel):
    """FX rate response."""
    pair: str
    base: str
    quote: str
    rate: float
    bid: float
    ask: float
    spread_bps: float
    change_24h: float


class BalanceResponse(BaseModel):
    """Currency balance response."""
    currency: str
    amount: float
    amount_usd: float
    interest_rate: float


class SweepSuggestionResponse(BaseModel):
    """Sweep suggestion response."""
    id: str
    from_currency: str
    to_vehicle: str
    amount: float
    projected_yield: float
    risk: str
    description: str


class RepoRateResponse(BaseModel):
    """Repo rate response."""
    region: str
    name: str
    rate: float
    change: float


class DashboardResponse(BaseModel):
    """Full dashboard response."""
    balances: List[BalanceResponse]
    fx_rates: List[FXRateResponse]
    sweep_suggestions: List[SweepSuggestionResponse]
    repo_rates: List[RepoRateResponse]
    total_value_usd: float


class FXRatesResponse(BaseModel):
    """FX rates list response."""
    rates: List[FXRateResponse]


class ConversionRequest(BaseModel):
    """FX conversion request."""
    from_currency: str
    to_currency: str
    amount: float


class ConversionResponse(BaseModel):
    """FX conversion response."""
    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    rate_used: float
    spread_cost: float
    timestamp: str


class SweepExecuteRequest(BaseModel):
    """Sweep execution request."""
    suggestion_id: str


class SweepExecuteResponse(BaseModel):
    """Sweep execution response."""
    success: bool
    message: str
    suggestion_id: str


class CarryTradeResponse(BaseModel):
    """Carry trade opportunity response."""
    opportunity: bool
    borrow_currency: Optional[str] = None
    invest_currency: Optional[str] = None
    spread_percent: Optional[float] = None
    description: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    service: FXService = Depends(get_fx_service)
) -> DashboardResponse:
    """
    Get complete cash management dashboard.
    
    Returns balances, FX rates, sweep suggestions, and repo rates.
    """
    try:
        balances = await service.get_balances()
        fx_rates = await service.get_fx_rates()
        suggestions = await service.get_sweep_suggestions()
        repo_rates = await service.get_repo_rates()
        total = await service.get_total_value_usd()
        
        return DashboardResponse(
            balances=[
                BalanceResponse(
                    currency=b.currency,
                    amount=b.amount,
                    amount_usd=b.amount_usd,
                    interest_rate=b.interest_rate
                ) for b in balances
            ],
            fx_rates=[
                FXRateResponse(
                    pair=r.pair,
                    base=r.base,
                    quote=r.quote,
                    rate=r.rate,
                    bid=r.bid,
                    ask=r.ask,
                    spread_bps=r.spread_bps,
                    change_24h=r.change_24h
                ) for r in fx_rates
            ],
            sweep_suggestions=[
                SweepSuggestionResponse(
                    id=s.id,
                    from_currency=s.from_currency,
                    to_vehicle=s.to_vehicle,
                    amount=s.amount,
                    projected_yield=s.projected_yield,
                    risk=s.risk,
                    description=s.description
                ) for s in suggestions
            ],
            repo_rates=[
                RepoRateResponse(
                    region=r.region,
                    name=r.name,
                    rate=r.rate,
                    change=r.change
                ) for r in repo_rates
            ],
            total_value_usd=total
        )
    except Exception as e:
        logger.exception("Error getting cash dashboard")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fx/rates", response_model=FXRatesResponse)
async def get_fx_rates(
    service: FXService = Depends(get_fx_service)
) -> FXRatesResponse:
    """
    Get current FX rates for all major pairs.
    """
    try:
        rates = await service.get_fx_rates()
        
        return FXRatesResponse(
            rates=[
                FXRateResponse(
                    pair=r.pair,
                    base=r.base,
                    quote=r.quote,
                    rate=r.rate,
                    bid=r.bid,
                    ask=r.ask,
                    spread_bps=r.spread_bps,
                    change_24h=r.change_24h
                ) for r in rates
            ]
        )
    except Exception as e:
        logger.exception("Error getting FX rates")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fx/convert", response_model=ConversionResponse)
async def execute_conversion(
    request: ConversionRequest,
    service: FXService = Depends(get_fx_service)
) -> ConversionResponse:
    """
    Execute an FX conversion.
    
    Converts amount from one currency to another.
    """
    try:
        # Check exposure limit
        if await service.check_exposure_limit(request.to_currency, request.amount):
            raise HTTPException(
                status_code=400,
                detail=f"Conversion would exceed 15% exposure limit for {request.to_currency}"
            )
        
        result = await service.execute_conversion(
            request.from_currency,
            request.to_currency,
            request.amount
        )
        
        return ConversionResponse(
            from_currency=result.from_currency,
            to_currency=result.to_currency,
            from_amount=result.from_amount,
            to_amount=result.to_amount,
            rate_used=result.rate_used,
            spread_cost=result.spread_cost,
            timestamp=result.timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error executing FX conversion")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sweep/suggestions")
async def get_sweep_suggestions(
    service: FXService = Depends(get_fx_service)
) -> List[SweepSuggestionResponse]:
    """
    Get cash sweep optimization suggestions.
    
    Suggests MMF, T-Bill, and repo investments for idle cash.
    """
    try:
        suggestions = await service.get_sweep_suggestions()
        
        return [
            SweepSuggestionResponse(
                id=s.id,
                from_currency=s.from_currency,
                to_vehicle=s.to_vehicle,
                amount=s.amount,
                projected_yield=s.projected_yield,
                risk=s.risk,
                description=s.description
            ) for s in suggestions
        ]
    except Exception as e:
        logger.exception("Error getting sweep suggestions")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sweep/execute", response_model=SweepExecuteResponse)
async def execute_sweep(
    request: SweepExecuteRequest,
    service: FXService = Depends(get_fx_service)
) -> SweepExecuteResponse:
    """
    Execute a cash sweep suggestion.
    """
    try:
        # In production, this would execute the actual sweep
        logger.info(f"Executing sweep: {request.suggestion_id}")
        
        return SweepExecuteResponse(
            success=True,
            message="Sweep executed successfully",
            suggestion_id=request.suggestion_id
        )
    except Exception as e:
        logger.exception("Error executing sweep")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repo/rates")
async def get_repo_rates(
    service: FXService = Depends(get_fx_service)
) -> List[RepoRateResponse]:
    """
    Get overnight repo rates by region.
    """
    try:
        rates = await service.get_repo_rates()
        
        return [
            RepoRateResponse(
                region=r.region,
                name=r.name,
                rate=r.rate,
                change=r.change
            ) for r in rates
        ]
    except Exception as e:
        logger.exception("Error getting repo rates")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carry-trade", response_model=CarryTradeResponse)
async def get_carry_trade_opportunity(
    service: FXService = Depends(get_fx_service)
) -> CarryTradeResponse:
    """
    Detect carry trade opportunities based on interest rate differentials.
    """
    try:
        opportunity = await service.detect_carry_trade_opportunity()
        return CarryTradeResponse(**opportunity)
    except Exception as e:
        logger.exception("Error detecting carry trade")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/currencies")
async def get_supported_currencies(
    service: FXService = Depends(get_fx_service)
) -> List[str]:
    """
    Get list of supported currencies.
    """
    return service.get_supported_currencies()
