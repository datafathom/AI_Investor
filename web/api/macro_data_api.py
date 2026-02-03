"""
==============================================================================
FILE: web/api/macro_data_api.py
ROLE: Macro Data REST API
PURPOSE: RESTful endpoints for FRED macroeconomic data consumption by frontend.
         Provides regime analysis, yield curve, and indicator endpoints.

INTEGRATION POINTS:
    - FredMacroService: Data source
    - MacroService: Regime analysis
    - macroStore.js: Frontend state management

ENDPOINTS:
    GET /api/v1/macro-data/regime - Current economic regime
    GET /api/v1/macro-data/yield-curve - Full yield curve
    GET /api/v1/macro-data/series/<series_id> - Historical series data
    GET /api/v1/macro-data/indicators - Key indicator summary
    GET /api/v1/macro-data/health - Data source health

AUTHENTICATION: JWT Bearer token recommended
RATE LIMITING: Inherits from APIGovernor (FRED limits)

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
import asyncio
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

macro_data_bp = Blueprint('macro_data', __name__, url_prefix='/api/v1/macro_data')


def _get_fred_service():
    """Lazy-load FRED service."""
    from services.data.fred_service import get_fred_service
    return get_fred_service()


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _build_response(data, source: str = "fred", cache_hit: bool = False):
    """Build standardized API response."""
    return {
        "data": data,
        "meta": {
            "request_id": str(hash(datetime.now())),
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "cache_hit": cache_hit,
        },
        "errors": []
    }


def _build_error_response(error_code: str, message: str, vendor: str = "fred"):
    """Build standardized error response."""
    return {
        "data": None,
        "meta": {
            "request_id": str(hash(datetime.now())),
            "timestamp": datetime.now().isoformat(),
            "source": vendor,
            "cache_hit": False,
        },
        "errors": [{
            "error_code": error_code,
            "message": message,
            "vendor": vendor
        }]
    }


# =============================================================================
# Regime Endpoint
# =============================================================================

@macro_data_bp.route('/regime', methods=['GET'])
def get_regime():
    """
    Retrieve current economic regime based on macro indicators.

    Returns:
        JSON with regime status, signals, metrics, and health score
    """
    try:
        service = _get_fred_service()
        regime = _run_async(service.get_macro_regime())

        return jsonify(_build_response({
            "status": regime.status,
            "signals": regime.signals,
            "metrics": regime.metrics,
            "health_score": regime.health_score,
            "timestamp": regime.timestamp.isoformat()
        }))

    except Exception as e:
        logger.error(f"Regime fetch failed: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch regime: {str(e)}"
        )), 500


# =============================================================================
# Yield Curve Endpoint
# =============================================================================

@macro_data_bp.route('/yield-curve', methods=['GET'])
def get_yield_curve():
    """
    Retrieve full yield curve data with all maturities.

    Returns:
        JSON with yields for each maturity (1M to 30Y)
    """
    try:
        service = _get_fred_service()
        curve = _run_async(service.get_yield_curve_data())

        if not curve:
            return jsonify(_build_error_response(
                "NO_DATA",
                "Unable to fetch yield curve data"
            )), 404

        # Calculate inversion status
        is_inverted = False
        if "2Y" in curve and "10Y" in curve:
            is_inverted = curve["10Y"] < curve["2Y"]

        return jsonify(_build_response({
            "curve": curve,
            "is_inverted": is_inverted,
            "spread_10y_2y": round(curve.get("10Y", 0) - curve.get("2Y", 0), 2) if "2Y" in curve and "10Y" in curve else None
        }))

    except Exception as e:
        logger.error(f"Yield curve fetch failed: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch yield curve: {str(e)}"
        )), 500


# =============================================================================
# Series Endpoint
# =============================================================================

@macro_data_bp.route('/series/<series_id>', methods=['GET'])
def get_series(series_id: str):
    """
    Retrieve historical data for a specific FRED series.

    Args:
        series_id: FRED series identifier (e.g., CPIAUCSL, UNRATE)

    Query Params:
        limit: Number of observations (default: 100)
        transform: Transformation type - "raw", "yoy", "mom" (default: raw)

    Returns:
        JSON array of observations with date and value
    """
    try:
        series_id = series_id.upper().strip()
        limit = request.args.get('limit', 100, type=int)
        transform_str = request.args.get('transform', 'raw').lower()

        from services.data.fred_service import TransformType
        transform_map = {
            "raw": TransformType.RAW,
            "yoy": TransformType.YOY,
            "mom": TransformType.MOM,
            "level": TransformType.LEVEL
        }

        transform = transform_map.get(transform_str, TransformType.RAW)

        service = _get_fred_service()
        data = _run_async(service.get_series(series_id, transform=transform, limit=limit))

        if not data:
            return jsonify(_build_error_response(
                "SERIES_NOT_FOUND",
                f"No data found for series: {series_id}"
            )), 404

        # Get metadata
        metadata = _run_async(service.get_series_metadata(series_id))

        return jsonify(_build_response({
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
        }))

    except Exception as e:
        logger.error(f"Series fetch failed for {series_id}: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch series: {str(e)}"
        )), 500


# =============================================================================
# Indicators Summary Endpoint
# =============================================================================

@macro_data_bp.route('/indicators', methods=['GET'])
def get_indicators():
    """
    Retrieve summary of key economic indicators.

    Returns:
        JSON with current values and YoY changes for major indicators
    """
    try:
        service = _get_fred_service()

        # Define indicators to fetch
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
            current = _run_async(service.get_latest_value(series_id))

            yoy_change = None
            if series_id in ["CPIAUCSL", "CPILFESL"]:
                yoy_change = _run_async(service.calculate_yoy_change(series_id))

            results.append({
                "name": name,
                "series_id": series_id,
                "value": current,
                "yoy_change": round(yoy_change, 2) if yoy_change else None,
                "units": "Percent" if series_id != "CPIAUCSL" else "Index"
            })

        return jsonify(_build_response({
            "indicators": results,
            "count": len(results)
        }))

    except Exception as e:
        logger.error(f"Indicators fetch failed: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch indicators: {str(e)}"
        )), 500


# =============================================================================
# Health Check Endpoint
# =============================================================================

@macro_data_bp.route('/health', methods=['GET'])
def get_health():
    """
    Get health status of FRED data source.

    Returns:
        JSON with status and API quota information
    """
    try:
        # Check APIGovernor for usage stats
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

        return jsonify(_build_response({
            "source": "FRED",
            "status": "online" if remaining_daily > 0 else "rate_limited",
            "requests_remaining": {
                "daily": max(0, remaining_daily),
                "per_minute": max(0, remaining_minute)
            }
        }))

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Health check failed: {str(e)}"
        )), 500
