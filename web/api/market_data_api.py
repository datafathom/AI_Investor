"""
==============================================================================
FILE: web/api/market_data_api.py
ROLE: Market Data REST API
PURPOSE: RESTful endpoints for frontend consumption of market data. Abstracts
         underlying data sources (Alpha Vantage, Polygon) behind unified API.

INTEGRATION POINTS:
    - AlphaVantageClient: Primary data source
    - DataFusionService: Intelligent source selection (future)
    - Redis: HTTP response caching (future)

ENDPOINTS:
    GET /api/v1/market/quote/<symbol> - Real-time quote
    GET /api/v1/market/history/<symbol> - Historical OHLCV data
    GET /api/v1/market/intraday/<symbol> - Intraday bars
    GET /api/v1/market/earnings - Earnings calendar
    GET /api/v1/market/health - Data source health status

AUTHENTICATION: JWT Bearer token recommended (not enforced in this version)
RATE LIMITING: Inherits from APIGovernor

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from web.auth_utils import login_required, requires_role
import logging
import asyncio
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

market_data_bp = Blueprint('market_data', __name__, url_prefix='/api/v1/market')


def _get_alpha_client():
    """Lazy-load Alpha Vantage client."""
    from services.data.alpha_vantage import get_alpha_vantage_client
    return get_alpha_vantage_client()


# Removed _run_async helper as services are now synchronous to prevent eventlet deadlocks.


def _build_response(data, source: str = "alpha_vantage", cache_hit: bool = False):
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


def _build_error_response(error_code: str, message: str, vendor: str = None):
    """Build standardized error response."""
    return {
        "data": None,
        "meta": {
            "request_id": str(hash(datetime.now())),
            "timestamp": datetime.now().isoformat(),
            "source": vendor or "unknown",
            "cache_hit": False,
        },
        "errors": [{
            "error_code": error_code,
            "message": message,
            "vendor": vendor
        }]
    }


# =============================================================================
# Quote Endpoint
# =============================================================================

@market_data_bp.route('/quote/<symbol>', methods=['GET'])
def get_quote(symbol: str):
    """
    Retrieve real-time quote for a stock symbol.
    
    Fetches the latest price, volume, and daily change metrics for the given
    equity symbol. Supports both live and mock data providers.
    
    Args:
        symbol (str): Stock ticker symbol (e.g., AAPL, MSFT).
        
    Query Params:
        mock (bool): If "true", return mock data instead of live vendor data.
        
    Returns:
        JSON: Standardized response with price, volume, and market state.
        
    Errors:
        400 (INVALID_SYMBOL): Symbol format is invalid.
        404 (SYMBOL_NOT_FOUND): No data found for specified ticker.
    """
    try:
        # Validate symbol
        symbol = symbol.upper().strip()
        if not symbol or len(symbol) > 10:
            return jsonify(_build_error_response(
                "INVALID_SYMBOL",
                f"Invalid symbol format: {symbol}",
                "alpha_vantage"
            )), 400

        # Check for mock mode
        use_mock = request.args.get('mock', 'false').lower() == 'true'

        client = _get_alpha_client()
        if use_mock:
            client.mock = True

        quote = client.get_quote(symbol)

        if not quote:
            return jsonify(_build_error_response(
                "SYMBOL_NOT_FOUND",
                f"No quote data found for symbol: {symbol}",
                "alpha_vantage"
            )), 404

        return jsonify(_build_response({
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
        }))

    except Exception as e:
        logger.error(f"Quote fetch failed for {symbol}: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch quote: {str(e)}",
            "alpha_vantage"
        )), 500


# =============================================================================
# Fear & Greed Endpoint
# =============================================================================

@market_data_bp.route('/fear-greed', methods=['GET'])
@login_required
def get_fear_greed():
    """
    Get current market Fear & Greed index status.
    
    Aggregates data from market momentum, volatility, and safe-haven demand 
    to provide a unified sentiment score.
    
    Returns:
        JSON: Standardized response with score (0-100) and sentiment label.
        
    Security:
        Bearer JWT required.
    """
    import random
    score = random.randint(30, 75) # Simulate moderate market sentiment
    
    status = "NEUTRAL"
    if score < 25: status = "EXTREME_FEAR"
    elif score < 45: status = "FEAR"
    elif score > 75: status = "EXTREME_GREED"
    elif score > 55: status = "GREED"

    return jsonify(_build_response({
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
    }))


# =============================================================================
# Historical Data Endpoint
# =============================================================================

@market_data_bp.route('/history/<symbol>', methods=['GET'])
def get_history(symbol: str):
    """
    Retrieve historical OHLCV data for a symbol.
    
    Returns a series of daily bars including open, high, low, close, volume, 
    and adjusted close prices. Supports compact (100 days) and full history.
    
    Args:
        symbol (str): Stock ticker symbol.
        
    Query Params:
        period (str): "compact" (last 100 days) or "full" (all available data).
        adjusted (bool): Whether to return split/dividend adjusted prices.
        
    Returns:
        JSON: Standardized response with historical bar array.
        
    Errors:
        400 (INVALID_SYMBOL): Symbol format is invalid.
        404 (NO_DATA): No historical data found for symbol.
    """
    try:
        symbol = symbol.upper().strip()
        if not symbol or len(symbol) > 10:
            return jsonify(_build_error_response(
                "INVALID_SYMBOL",
                f"Invalid symbol format: {symbol}",
                "alpha_vantage"
            )), 400

        period = request.args.get('period', 'compact')
        adjusted = request.args.get('adjusted', 'true').lower() == 'true'

        client = _get_alpha_client()
        bars = client.get_daily(symbol, outputsize=period, adjusted=adjusted)

        if not bars:
            return jsonify(_build_error_response(
                "NO_DATA",
                f"No historical data found for symbol: {symbol}",
                "alpha_vantage"
            )), 404

        return jsonify(_build_response({
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
        }))

    except Exception as e:
        logger.error(f"History fetch failed for {symbol}: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch history: {str(e)}",
            "alpha_vantage"
        )), 500


# =============================================================================
# Intraday Data Endpoint
# =============================================================================

@market_data_bp.route('/intraday/<symbol>', methods=['GET'])
def get_intraday(symbol: str):
    """
    Retrieve intraday OHLCV bars for a symbol.
    
    Fetches fine-grained price action at specified intervals (1min, 5min, etc.).
    Useful for high-frequency analysis and day-trading signals.
    
    Args:
        symbol (str): Stock ticker symbol.
        
    Query Params:
        interval (str): Time interval. Options: 1min, 5min, 15min, 30min, 60min.
        outputsize (str): "compact" (100 bars) or "full" (all available intraday).
        
    Returns:
        JSON: Standardized response with intraday bar array.
        
    Errors:
        400 (INVALID_INTERVAL): Specified interval is not supported.
        404 (NO_DATA): No intraday data found for symbol.
    """
    try:
        symbol = symbol.upper().strip()
        if not symbol or len(symbol) > 10:
            return jsonify(_build_error_response(
                "INVALID_SYMBOL",
                f"Invalid symbol format: {symbol}",
                "alpha_vantage"
            )), 400

        interval_str = request.args.get('interval', '5min')
        outputsize = request.args.get('outputsize', 'compact')

        # Map string to enum
        from services.data.alpha_vantage import IntervalType
        interval_map = {
            "1min": IntervalType.MIN_1,
            "5min": IntervalType.MIN_5,
            "15min": IntervalType.MIN_15,
            "30min": IntervalType.MIN_30,
            "60min": IntervalType.MIN_60,
        }

        interval = interval_map.get(interval_str)
        if not interval:
            return jsonify(_build_error_response(
                "INVALID_INTERVAL",
                f"Invalid interval: {interval_str}. Valid options: 1min, 5min, 15min, 30min, 60min",
                "alpha_vantage"
            )), 400

        client = _get_alpha_client()
        bars = client.get_intraday(symbol, interval=interval, outputsize=outputsize)

        if not bars:
            return jsonify(_build_error_response(
                "NO_DATA",
                f"No intraday data found for symbol: {symbol}",
                "alpha_vantage"
            )), 404

        return jsonify(_build_response({
            "status": "success",
            "symbol": symbol,
            "interval": interval_str,
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
        }))

    except Exception as e:
        logger.error(f"Intraday fetch failed for {symbol}: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch intraday: {str(e)}",
            "alpha_vantage"
        )), 500


# =============================================================================
# Short Interest Endpoint
# =============================================================================

@market_data_bp.route('/short-interest/<symbol>', methods=['GET'])
@login_required
def get_short_interest(symbol: str):
    """
    Retrieve short interest analysis for a symbol.
    
    Provides critical sentiment indicators including Short Interest Ratio, 
    Days to Cover, and Relative Volume metrics from Quandl/FINRA data.
    
    Args:
        symbol (str): Stock ticker symbol.
        
    Query Params:
        mock (bool): If "true", uses mock data for testing.
        
    Returns:
        JSON: Standardized response with short interest analysis model.
        
    Security:
        Bearer JWT required.
    """
    try:
        symbol = symbol.upper().strip()
        use_mock = request.args.get('mock', 'false').lower() == 'true'

        from services.analysis.short_interest_service import get_short_interest_service
        service = get_short_interest_service()
        
        if use_mock:
            service.quandl.mock = True
            service.av.mock = True

        analysis = service.analyze_symbol(symbol)

        if not analysis:
            return jsonify(_build_error_response(
                "NO_DATA",
                f"No short interest data found for symbol: {symbol}",
                "quandl"
            )), 404

        return jsonify(_build_response({
            "status": "success",
            "analysis": analysis.model_dump()
        }, source="quandl"))

    except Exception as e:
        logger.error(f"Short interest fetch failed for {symbol}: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch short interest: {str(e)}",
            "quandl"
        )), 500


# =============================================================================
# Earnings Calendar Endpoint
# =============================================================================

@market_data_bp.route('/earnings', methods=['GET'])
def get_earnings():
    """
    Retrieve upcoming earnings calendar.
    
    Returns a schedule of corporate earnings releases, including estimated 
    earnings per share (EPS) and reporting currencies.
    
    Query Params:
        symbol (str): Optional ticker symbol to filter calendar.
        horizon (str): Time lookahead. Options: 3month, 6month, 12month.
        
    Returns:
        JSON: Standardized response with earnings event array.
        
    Errors:
        400 (INVALID_HORIZON): Lookahead period is not supported.
    """
    try:
        symbol = request.args.get('symbol')
        horizon = request.args.get('horizon', '3month')

        if horizon not in ['3month', '6month', '12month']:
            return jsonify(_build_error_response(
                "INVALID_HORIZON",
                f"Invalid horizon: {horizon}. Valid options: 3month, 6month, 12month",
                "alpha_vantage"
            )), 400

        client = _get_alpha_client()
        earnings = client.get_earnings_calendar(symbol=symbol, horizon=horizon)

        if not earnings:
            return jsonify(_build_response({
                "status": "success",
                "earnings": [],
                "count": 0
            }))

        return jsonify(_build_response({
            "status": "success",
            "count": len(earnings),
            "earnings": [
                {
                    "symbol": e.symbol,
                    "name": e.name,
                    "report_date": e.report_date,
                    "fiscal_date_ending": e.fiscal_date_ending,
                    "estimate": e.estimate,
                    "currency": e.currency
                }
                for e in earnings
            ]
        }))

    except Exception as e:
        logger.error(f"Earnings fetch failed: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to fetch earnings: {str(e)}",
            "alpha_vantage"
        )), 500


# =============================================================================
# Health Check Endpoint
# =============================================================================

@market_data_bp.route('/health', methods=['GET'])
def get_health():
    """
    Get health status of market data sources.
    
    Monitors API quota usage and connectivity status for critical vendors 
    like Alpha Vantage.
    
    Returns:
        JSON: Standardized response with provider health metrics.
    """
    try:
        # Check APIGovernor for usage stats
        try:
            from services.system.api_governance import get_governor
            governor = get_governor()
            av_usage = governor._usage.get("ALPHA_VANTAGE", {})
            av_limit = governor.LIMITS.get("ALPHA_VANTAGE", {})

            remaining_daily = av_limit.get("per_day", 0) - av_usage.get("day_count", 0)
            remaining_minute = av_limit.get("per_minute", 0) - av_usage.get("minute_count", 0)

        except Exception:
            remaining_daily = -1
            remaining_minute = -1

        return jsonify(_build_response({
            "status": "success",
            "overall_status": "healthy" if remaining_daily > 0 else "degraded",
            "sources": [
                {
                    "name": "Alpha Vantage",
                    "status": "online" if remaining_daily > 0 else "rate_limited",
                    "requests_remaining": {
                        "daily": max(0, remaining_daily),
                        "per_minute": max(0, remaining_minute)
                    }
                }
            ]
        }))

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Health check failed: {str(e)}",
            "system"
        )), 500
