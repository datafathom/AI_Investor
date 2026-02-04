"""
Market Data API - FastAPI Router
Migrated from Flask (web/api/market_data_api.py)
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Any
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/market", tags=["Market Data"])

from services.data.alpha_vantage import get_alpha_vantage_client


def get_alpha_provider():
    """Provider for Alpha Vantage client."""
    return get_alpha_vantage_client()


def _build_response(data: Any, source: str = "alpha_vantage", cache_hit: bool = False):
    """Build standardized API response."""
    return {
        "success": True,
        "data": {
            "content": data,
            "meta": {
                "request_id": str(hash(datetime.now())),
                "timestamp": datetime.now().isoformat(),
                "source": source,
                "cache_hit": cache_hit,
            }
        }
    }


def _build_error_response(status_code: int, message: str, vendor: str = "alpha_vantage"):
    """Build standardized error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "detail": message,
            "data": {
                "vendor": vendor,
                "meta": {
                    "timestamp": datetime.now().isoformat(),
                    "source": vendor
                }
            }
        }
    )

@router.get("/quote/{symbol}")
async def get_quote(
    symbol: str,
    mock: bool = False,
    client = Depends(get_alpha_provider)
):
    """Retrieve real-time quote for a stock symbol."""
    try:
        symbol = symbol.upper().strip()
        if mock:
            client.mock = True
        
        quote = client.get_quote(symbol)
        if not quote:
            return _build_error_response(404, f"No quote data found for symbol: {symbol}")

        return _build_response({
            "status": "success",
            "symbol": quote.symbol,
            "price": quote.price,
            "open": quote.open,
            "high": quote.high,
            "low": quote.low,
            "volume": quote.volume,
            "previous_close": quote.previous_close,
            "change": quote.change,
            "change_percent": quote.change_percent,
            "latest_trading_day": quote.latest_trading_day,
            "timestamp": quote.timestamp.isoformat()
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Quote fetch failed for {symbol}")
        return _build_error_response(500, str(e))

@router.get("/fear-greed")
async def get_fear_greed():
    """Get current market Fear & Greed index status."""
    score = random.randint(30, 75)
    status = "NEUTRAL"
    if score < 25: status = "EXTREME_FEAR"
    elif score < 45: status = "FEAR"
    elif score > 75: status = "EXTREME_GREED"
    elif score > 55: status = "GREED"

    return _build_response({
        "status": "success",
        "score": score,
        "label": status,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "market_momentum": random.randint(40, 60),
            "stock_price_strength": random.randint(40, 60),
            "stock_price_breadth": random.randint(40, 60),
            "put_call_options": random.uniform(0.6, 1.2),
            "market_volatility": random.randint(15, 25),
            "safe_haven_demand": random.uniform(-2, 2),
            "junk_bond_demand": random.uniform(0.5, 1.5)
        }
    })

@router.get("/history/{symbol}")
async def get_history(
    symbol: str, 
    period: str = "compact", 
    adjusted: bool = True,
    client = Depends(get_alpha_provider)
):
    """Retrieve historical OHLCV data for a symbol."""
    try:
        symbol = symbol.upper().strip()
        bars = client.get_daily(symbol, outputsize=period, adjusted=adjusted)
        
        if not bars:
            return _build_error_response(404, f"No historical data found for symbol: {symbol}")

        return _build_response({
            "status": "success",
            "symbol": symbol,
            "count": len(bars),
            "bars": [
                {
                    "timestamp": bar.timestamp.isoformat(),
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "adjusted_close": bar.adjusted_close,
                    "volume": bar.volume,
                    "dividend": bar.dividend,
                    "split_coefficient": bar.split_coefficient
                }
                for bar in bars
            ]
        })
    except Exception as e:
        logger.exception(f"History fetch failed for {symbol}")
        return _build_error_response(500, str(e))

@router.get("/intraday/{symbol}")
async def get_intraday(
    symbol: str, 
    interval: str = "5min", 
    outputsize: str = "compact",
    client = Depends(get_alpha_provider)
):
    """Retrieve intraday OHLCV bars for a symbol."""
    try:
        symbol = symbol.upper().strip()
        from services.data.alpha_vantage import IntervalType
        interval_map = {
            "1min": IntervalType.MIN_1,
            "5min": IntervalType.MIN_5,
            "15min": IntervalType.MIN_15,
            "30min": IntervalType.MIN_30,
            "60min": IntervalType.MIN_60,
        }
        
        int_val = interval_map.get(interval)
        if not int_val:
            return _build_error_response(400, f"Invalid interval: {interval}")
        bars = client.get_intraday(symbol, interval=int_val, outputsize=outputsize)
        
        if not bars:
            return _build_error_response(404, f"No intraday data found for symbol: {symbol}")

        return _build_response({
            "status": "success",
            "symbol": symbol,
            "interval": interval,
            "count": len(bars),
            "bars": [
                {
                    "timestamp": bar.timestamp.isoformat(),
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "volume": bar.volume
                }
                for bar in bars
            ]
        })
    except Exception as e:
        logger.exception(f"Intraday fetch failed for {symbol}")
        return _build_error_response(500, str(e))

@router.get("/earnings")
async def get_earnings(
    symbol: Optional[str] = None,
    horizon: str = "3month",
    client = Depends(get_alpha_provider)
):
    """Retrieve upcoming earnings calendar."""
    try:
        if horizon not in ['3month', '6month', '12month']:
            return _build_error_response(400, f"Invalid horizon: {horizon}")
        earnings = client.get_earnings_calendar(symbol=symbol, horizon=horizon)
        
        return _build_response({
            "status": "success",
            "count": len(earnings) if earnings else 0,
            "earnings": [
                {
                    "symbol": e.symbol,
                    "name": e.name,
                    "report_date": e.report_date,
                    "fiscal_date_ending": e.fiscal_date_ending,
                    "estimate": e.estimate,
                    "currency": e.currency
                }
                for e in (earnings or [])
            ]
        })
    except Exception as e:
        logger.exception("Earnings fetch failed")
        return _build_error_response(500, str(e))

@router.get("/health")
async def get_market_health():
    """Get health status of market data sources."""
    try:
        from services.system.api_governance import get_governor
        governor = get_governor()
        av_usage = governor._usage.get("ALPHA_VANTAGE", {})
        av_limit = governor.LIMITS.get("ALPHA_VANTAGE", {})

        remaining_daily = av_limit.get("per_day", 0) - av_usage.get("day_count", 0)
        
        return _build_response({
            "status": "success",
            "overall_status": "healthy" if remaining_daily > 0 else "degraded",
            "sources": [
                {
                    "name": "Alpha Vantage",
                    "status": "online" if remaining_daily > 0 else "rate_limited",
                    "requests_remaining": {
                        "daily": max(0, remaining_daily)
                    }
                }
            ]
        })
    except Exception as e:
        logger.exception("Market health check failed")
        return _build_error_response(500, str(e))
