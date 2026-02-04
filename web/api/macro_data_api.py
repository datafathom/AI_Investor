"""
==============================================================================
FILE: web/api/macro_data_api.py
ROLE: Macro Data REST API (FastAPI)
PURPOSE: RESTful endpoints for FRED macroeconomic data consumption by frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from services.data.fred_service import TransformType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/macro_data", tags=["Macro Data"])
# Hyphenated alias router for frontend compatibility
router_hyphen = APIRouter(prefix="/api/v1/macro-data", tags=["Macro Data"])


from services.data.fred_service import get_fred_service


def get_fred_provider():
    """Provider for FRED service."""
    return get_fred_service()


def _build_response(data, source: str = "fred", cache_hit: bool = False):
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


def _build_error_response(status_code: int, error_code: str, message: str, vendor: str = "fred"):
    """Build standardized error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "detail": message,
            "data": {
                "error_code": error_code,
                "vendor": vendor,
                "meta": {
                    "timestamp": datetime.now().isoformat(),
                    "source": vendor,
                }
            }
        }
    )


@router.get("/regime")
@router_hyphen.get("/regime")
async def get_regime(service = Depends(get_fred_provider)):
    """Retrieve current economic regime based on macro indicators."""
    try:
        regime = await service.get_macro_regime()

        return _build_response({
            "status": regime.status,
            "signals": regime.signals,
            "metrics": regime.metrics,
            "health_score": regime.health_score,
            "timestamp": regime.timestamp.isoformat()
        })
    except Exception as e:
        logger.exception("Regime fetch failed")
        return _build_error_response(500, "INTERNAL_ERROR", f"Failed to fetch regime: {str(e)}")


@router.get("/yield-curve")
@router_hyphen.get("/yield-curve")
async def get_yield_curve(service = Depends(get_fred_provider)):
    """Retrieve full yield curve data with all maturities."""
    try:
        curve = await service.get_yield_curve_data()

        if not curve:
            return _build_error_response(404, "NO_DATA", "Unable to fetch yield curve data")

        is_inverted = False
        if "2Y" in curve and "10Y" in curve:
            is_inverted = curve["10Y"] < curve["2Y"]

        return _build_response({
            "curve": curve,
            "is_inverted": is_inverted,
            "spread_10y_2y": round(curve.get("10Y", 0) - curve.get("2Y", 0), 2) if "2Y" in curve and "10Y" in curve else None
        })
    except Exception as e:
        logger.exception("Yield curve fetch failed")
        return _build_error_response(500, "INTERNAL_ERROR", f"Failed to fetch yield curve: {str(e)}")


@router.get("/series/{series_id}")
@router_hyphen.get("/series/{series_id}")
async def get_series(
    series_id: str,
    limit: int = Query(100),
    transform_str: str = Query("raw", alias="transform"),
    service = Depends(get_fred_provider)
):
    """Retrieve historical data for a specific FRED series."""
    try:
        series_id = series_id.upper().strip()
        
        transform_map = {
            "raw": TransformType.RAW,
            "yoy": TransformType.YOY,
            "mom": TransformType.MOM,
            "level": TransformType.LEVEL
        }

        transform = transform_map.get(transform_str.lower(), TransformType.RAW)
        data = await service.get_series(series_id, transform=transform, limit=limit)

        if not data:
            return _build_error_response(404, "SERIES_NOT_FOUND", f"No data found for series: {series_id}")

        metadata = await service.get_series_metadata(series_id)

        return _build_response({
            "series_id": series_id,
            "title": metadata.title if metadata else series_id,
            "units": metadata.units if metadata else "Units",
            "frequency": metadata.frequency if metadata else "Unknown",
            "transform": transform_str,
            "observations": [
                {"date": dp.date, "value": dp.value}
                for dp in data if dp.value is not None
            ],
            "count": len([dp for dp in data if dp.value is not None])
        })
    except Exception as e:
        logger.exception(f"Series fetch failed for {series_id}")
        return _build_error_response(500, "INTERNAL_ERROR", f"Failed to fetch series: {str(e)}")


@router.get("/indicators")
@router_hyphen.get("/indicators")
async def get_indicators(service = Depends(get_fred_provider)):
    """Retrieve summary of key economic indicators."""
    try:

        indicators = [
            ("CPI", "CPIAUCSL"),
            ("Unemployment", "UNRATE"),
            ("Fed Funds", "FEDFUNDS"),
            ("VIX", "VIXCLS"),
            ("10Y-2Y Spread", "T10Y2Y"),
            ("GDP Growth", "A191RL1Q225SBEA")
        ]

        results = []
        for name, series_id in indicators:
            current = await service.get_latest_value(series_id)

            yoy_change = None
            if series_id in ["CPIAUCSL", "CPILFESL"]:
                yoy_change = await service.calculate_yoy_change(series_id)

            results.append({
                "name": name,
                "series_id": series_id,
                "value": current,
                "yoy_change": round(yoy_change, 2) if yoy_change else None,
                "units": "Percent" if series_id != "CPIAUCSL" else "Index"
            })

        return _build_response({
            "indicators": results,
            "count": len(results)
        })
    except Exception as e:
        logger.exception("Indicators fetch failed")
        return _build_error_response(500, "INTERNAL_ERROR", f"Failed to fetch indicators: {str(e)}")


@router.get("/health")
@router_hyphen.get("/health")
async def get_health():
    """Get health status of FRED data source."""
    try:
        try:
            from services.system.api_governance import get_governor
            governor = get_governor()
            fred_usage = governor._usage.get("FRED", {})
            fred_limit = governor.LIMITS.get("FRED", {})

            remaining_daily = fred_limit.get("per_day", 0) - fred_usage.get("day_count", 0)
            remaining_minute = fred_limit.get("per_minute", 0) - fred_usage.get("minute_count", 0)

        except Exception:
            remaining_daily = -1
            remaining_minute = -1

        return _build_response({
            "source": "FRED",
            "status": "online" if remaining_daily > 0 else "rate_limited",
            "requests_remaining": {
                "daily": max(0, remaining_daily),
                "per_minute": max(0, remaining_minute)
            }
        })
    except Exception as e:
        logger.exception("Health check failed")
        return _build_error_response(500, "INTERNAL_ERROR", f"Health check failed: {str(e)}")
