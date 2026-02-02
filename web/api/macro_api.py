"""
Macro API - REST endpoints for global macroeconomic data.

Phase 53: Provides endpoints for political trading, CPI data,
world map visualization, and futures curves.

Endpoints:
    GET  /api/v1/macro/insider-trades      - Political insider trades
    GET  /api/v1/macro/cpi/<country>       - CPI data by country
    GET  /api/v1/macro/correlations        - Inflation hedge correlations
    GET  /api/v1/macro/world-map           - World map data
    GET  /api/v1/macro/calendar            - Economic events calendar
    GET  /api/v1/macro/futures/<commodity> - Futures curve
    GET  /api/v1/macro/crack-spread        - Crack spread calculation
"""

from flask import Blueprint, jsonify, request
from services.analysis.macro_service import MacroService
from services.market.futures_service import FuturesService
import logging

logger = logging.getLogger(__name__)

macro_bp = Blueprint('macro', __name__)
_macro_service = MacroService()
_futures_service = FuturesService()


@macro_bp.route('/insider-trades', methods=['GET'])
async def get_insider_trades():
    """Get political insider trading data."""
    try:
        region = request.args.get('region')
        trades = await _macro_service.get_political_insider_trades(region)
        
        return jsonify({
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
        })
        
    except Exception as e:
        logger.error(f"Insider trades fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/cpi/<country>', methods=['GET'])
async def get_cpi(country: str):
    """Get CPI data for a country."""
    try:
        cpi = await _macro_service.get_regional_cpi(country)
        
        return jsonify({
            "success": True,
            "data": {
                "country_code": cpi.country_code,
                "country_name": cpi.country_name,
                "current_cpi": cpi.current_cpi,
                "yoy_change": cpi.yoy_change,
                "core_cpi": cpi.core_cpi,
                "updated_at": cpi.updated_at
            }
        })
        
    except Exception as e:
        logger.error(f"CPI fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/correlations', methods=['GET'])
async def get_correlations():
    """Get inflation hedge correlation matrix."""
    try:
        matrix = await _macro_service.get_inflation_hedge_correlations()
        
        return jsonify({
            "success": True,
            "data": {
                "assets": matrix.assets,
                "correlations": matrix.correlations,
                "best_hedge": matrix.best_hedge,
                "worst_hedge": matrix.worst_hedge
            }
        })
        
    except Exception as e:
        logger.error(f"Correlations fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/world-map', methods=['GET'])
async def get_world_map():
    """Get data for world map visualization."""
    try:
        data = await _macro_service.get_world_map_data()
        
        return jsonify({
            "success": True,
            "data": data
        })
        
    except Exception as e:
        logger.error(f"World map data fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/calendar', methods=['GET'])
async def get_calendar():
    """Get economic events calendar."""
    try:
        days = request.args.get('days', 7, type=int)
        events = await _macro_service.get_economic_calendar(days)
        
        return jsonify({
            "success": True,
            "data": events
        })
        
    except Exception as e:
        logger.error(f"Calendar fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/futures/<commodity>', methods=['GET'])
async def get_futures_curve(commodity: str):
    """Get futures curve for a commodity."""
    try:
        curve = await _futures_service.get_futures_curve(commodity)
        roll_yield = await _futures_service.calculate_roll_yield(curve)
        
        return jsonify({
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
        })
        
    except Exception as e:
        logger.error(f"Futures curve fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/futures', methods=['GET'])
async def get_all_futures():
    """Get futures curves for all commodities."""
    try:
        curves = await _futures_service.get_all_curves()
        
        return jsonify({
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
        })
        
    except Exception as e:
        logger.error(f"Futures curves fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/crack-spread', methods=['GET'])
async def get_crack_spread():
    """Get crack spread calculation."""
    try:
        spread = await _futures_service.calculate_crack_spread()
        
        return jsonify({
            "success": True,
            "data": {
                "name": spread.name,
                "value": spread.value,
                "historical_mean": spread.historical_mean,
                "z_score": spread.z_score,
                "components": spread.components
            }
        })
        
    except Exception as e:
        logger.error(f"Crack spread fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/dashboard', methods=['GET'])
async def get_macro_dashboard():
    """Combined dashboard data for the frontend."""
    try:
        world_map = await _macro_service.get_world_map_data()
        political = await _macro_service.get_political_insider_trades()
        # Mocking shipping/commodities as they are secondary to core macro
        shipping = [
            {"route": "Suez Canal", "volume": 850000, "change": -12, "status": "congested"},
            {"route": "Panama Canal", "volume": 420000, "change": -2, "status": "normal"}
        ]
        commodities = [
            {"name": "Crude Oil", "price": 74.5, "change": 1.2, "unit": "barrel"},
            {"name": "Gold", "price": 2045.0, "change": -0.5, "unit": "oz"}
        ]
        
        return jsonify({
            "success": True,
            "world_map_data": world_map,
            "political_signals": [
                {"region": t.country, "signal": "BULLISH" if t.action == "BUY" else "BEARISH", "reason": f"Political {t.action} of {t.ticker}", "source": t.politician}
                for t in political
            ],
            "shipping_routes": shipping,
            "commodities": commodities
        })
    except Exception as e:
        logger.error(f"Macro dashboard fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@macro_bp.route('/regime', methods=['GET'])
async def get_macro_regime():
    """Get the current economic regime classification."""
    try:
        regime = await _macro_service._fred.get_macro_regime()
        return jsonify({
            "success": True,
            "data": {
                "status": regime.status,
                "signals": regime.signals,
                "metrics": regime.metrics,
                "health_score": regime.health_score,
                "timestamp": regime.timestamp.isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Regime detection failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
