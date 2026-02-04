"""
Macro API - REST endpoints for global macroeconomic data. (FastAPI)

Phase 53: Provides endpoints for political trading, CPI data,
world map visualization, and futures curves.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging
from typing import Optional, List, Dict, Any

from services.analysis.macro_service import MacroService
from services.market.futures_service import FuturesService


def get_macro_provider() -> MacroService:
    return MacroService()


def get_futures_provider() -> FuturesService:
    return FuturesService()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/macro", tags=["Macro"])



@router.get("/insider-trades")
async def get_insider_trades(
    region: Optional[str] = Query(None),
    macro_service: MacroService = Depends(get_macro_provider)
):
    """Get political insider trading data."""
    try:
        trades = await macro_service.get_political_insider_trades(region)
        
        return {
            "success": True,
            "data": [
                {
                    "politician": t.politician,
                    "party": t.party,
                    "country": t.country,
                    "ticker": t.ticker,
                    "action": t.action,
                    "amount": t.amount,
                    "trade_date": t.trade_date,
                    "disclosure_date": t.disclosure_date,
                    "delay_days": t.delay_days
                }
                for t in trades
            ]
        }
    except Exception as e:
        logger.exception("Insider trades fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/cpi/{country}")
async def get_cpi(
    country: str,
    macro_service: MacroService = Depends(get_macro_provider)
):
    """Get CPI data for a country."""
    try:
        cpi = await macro_service.get_regional_cpi(country)
        
        return {
            "success": True,
            "data": {
                "country_code": cpi.country_code,
                "country_name": cpi.country_name,
                "current_cpi": cpi.current_cpi,
                "yoy_change": cpi.yoy_change,
                "core_cpi": cpi.core_cpi,
                "updated_at": cpi.updated_at
            }
        }
    except Exception as e:
        logger.exception("CPI fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/correlations")
async def get_correlations(macro_service: MacroService = Depends(get_macro_provider)):
    """Get inflation hedge correlation matrix."""
    try:
        matrix = await macro_service.get_inflation_hedge_correlations()
        
        return {
            "success": True,
            "data": {
                "assets": matrix.assets,
                "correlations": matrix.correlations,
                "best_hedge": matrix.best_hedge,
                "worst_hedge": matrix.worst_hedge
            }
        }
    except Exception as e:
        logger.exception("Correlations fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/world-map")
async def get_world_map(macro_service: MacroService = Depends(get_macro_provider)):
    """Get data for world map visualization."""
    try:
        data = await macro_service.get_world_map_data()
        
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.exception("World map data fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/calendar")
async def get_calendar(
    days: int = Query(7),
    macro_service: MacroService = Depends(get_macro_provider)
):
    """Get economic events calendar."""
    try:
        events = await macro_service.get_economic_calendar(days)
        
        return {
            "success": True,
            "data": events
        }
    except Exception as e:
        logger.exception("Calendar fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/futures/{commodity}")
async def get_futures_curve(
    commodity: str,
    futures_service: FuturesService = Depends(get_futures_provider)
):
    """Get futures curve for a commodity."""
    try:
        curve = await futures_service.get_futures_curve(commodity)
        roll_yield = await futures_service.calculate_roll_yield(curve)
        
        return {
            "success": True,
            "data": {
                "commodity": curve.commodity,
                "commodity_name": curve.commodity_name,
                "spot_price": curve.spot_price,
                "curve_shape": curve.curve_shape,
                "roll_yield_annual": roll_yield,
                "contracts": [
                    {
                        "symbol": c.symbol,
                        "expiry_date": c.expiry_date,
                        "price": c.price,
                        "volume": c.volume,
                        "open_interest": c.open_interest
                    }
                    for c in curve.contracts
                ],
                "updated_at": curve.updated_at
            }
        }
    except Exception as e:
        logger.exception("Futures curve fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/futures")
async def get_all_futures(futures_service: FuturesService = Depends(get_futures_provider)):
    """Get futures curves for all commodities."""
    try:
        curves = await futures_service.get_all_curves()
        
        return {
            "success": True,
            "data": [
                {
                    "commodity": c.commodity,
                    "name": c.commodity_name,
                    "spot_price": c.spot_price,
                    "curve_shape": c.curve_shape
                }
                for c in curves
            ]
        }
    except Exception as e:
        logger.exception("Futures curves fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/crack-spread")
async def get_crack_spread(futures_service: FuturesService = Depends(get_futures_provider)):
    """Get crack spread calculation."""
    try:
        spread = await futures_service.calculate_crack_spread()
        
        return {
            "success": True,
            "data": {
                "name": spread.name,
                "value": spread.value,
                "historical_mean": spread.historical_mean,
                "z_score": spread.z_score,
                "components": spread.components
            }
        }
    except Exception as e:
        logger.exception("Crack spread fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/dashboard")
async def get_macro_dashboard(macro_service: MacroService = Depends(get_macro_provider)):
    """Combined dashboard data for the frontend."""
    try:
        world_map = await macro_service.get_world_map_data()
        political = await macro_service.get_political_insider_trades()
        
        shipping = [
            {"route": "Suez Canal", "volume": 850000, "change": -12, "status": "congested"},
            {"route": "Panama Canal", "volume": 420000, "change": -2, "status": "normal"}
        ]
        commodities = [
            {"name": "Crude Oil", "price": 74.5, "change": 1.2, "unit": "barrel"},
            {"name": "Gold", "price": 2045.0, "change": -0.5, "unit": "oz"}
        ]
        
        return {
            "success": True,
            "data": {
                "world_map_data": world_map,
                "political_signals": [
                    {"region": t.country, "signal": "BULLISH" if t.action == "BUY" else "BEARISH", "reason": f"Political {t.action} of {t.ticker}", "source": t.politician}
                    for t in political
                ],
                "shipping_routes": shipping,
                "commodities": commodities
            }
        }
    except Exception as e:
        logger.exception("Macro dashboard fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/regime")
async def get_macro_regime(macro_service: MacroService = Depends(get_macro_provider)):
    """Get the current economic regime classification."""
    try:
        regime = await macro_service._fred.get_macro_regime()
        return {
            "success": True,
            "data": {
                "status": regime.status,
                "signals": regime.signals,
                "metrics": regime.metrics,
                "health_score": regime.health_score,
                "timestamp": regime.timestamp.isoformat()
            }
        }
    except Exception as e:
        logger.exception("Regime detection failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
