"""
Fixed Income API - REST endpoints for bond analytics and yield curve.

Phase 50: Provides endpoints for bond ladder management, duration analysis,
rate shock simulation, and yield curve visualization.

Endpoints:
    GET  /api/v1/fixed-income/yield-curve          - Current yield curve
    GET  /api/v1/fixed-income/yield-curve/history  - Historical curves
    POST /api/v1/fixed-income/rate-shock           - Rate shock simulation
    POST /api/v1/fixed-income/duration             - Calculate bond duration
    POST /api/v1/fixed-income/wal                  - Calculate WAL
    GET  /api/v1/fixed-income/gaps/<portfolio_id>  - Liquidity gap analysis
"""

from flask import Blueprint, jsonify, request
from services.analysis.fixed_income_service import (
    FixedIncomeService,
    Bond,
    BondType
)
import logging

logger = logging.getLogger(__name__)

fixed_income_bp = Blueprint('fixed_income', __name__)
_service = FixedIncomeService()


@fixed_income_bp.route('/yield-curve', methods=['GET'])
async def get_yield_curve():
    """Get current Treasury yield curve."""
    try:
        curve = await _service.get_yield_curve()
        
        return jsonify({
            "success": True,
            "data": {
                "date": curve.date,
                "rates": curve.rates,
                "is_inverted": curve.is_inverted
            }
        })
        
    except Exception as e:
        logger.error(f"Yield curve fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@fixed_income_bp.route('/yield-curve/history', methods=['GET'])
async def get_yield_curve_history():
    """Get historical yield curves for animation."""
    try:
        months = request.args.get('months', 12, type=int)
        curves = await _service.get_historical_curves(months)
        
        return jsonify({
            "success": True,
            "data": [
                {
                    "date": c.date,
                    "rates": c.rates,
                    "is_inverted": c.is_inverted
                }
                for c in curves
            ]
        })
        
    except Exception as e:
        logger.error(f"Historical curves fetch failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@fixed_income_bp.route('/rate-shock', methods=['POST'])
async def simulate_rate_shock():
    """
    Simulate rate shock impact on portfolio.
    
    Request Body:
        portfolio_id: Portfolio to analyze
        basis_points: Rate shock in basis points (e.g., 100 = +1%)
    """
    try:
        data = request.get_json()
        portfolio_id = data.get('portfolio_id', 'default')
        basis_points = data.get('basis_points', 100)
        
        impact = await _service.get_rate_shock_impact(portfolio_id, basis_points)
        
        return jsonify({
            "success": True,
            "data": {
                "shock_basis_points": impact.shock_basis_points,
                "portfolio_value_before": impact.portfolio_value_before,
                "portfolio_value_after": impact.portfolio_value_after,
                "dollar_change": impact.dollar_change,
                "percentage_change": impact.percentage_change
            }
        })
        
    except Exception as e:
        logger.error(f"Rate shock simulation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@fixed_income_bp.route('/duration', methods=['POST'])
async def calculate_duration():
    """
    Calculate duration metrics for a bond.
    
    Request Body:
        par_value: Face value
        coupon_rate: Annual coupon rate (decimal)
        maturity_years: Years to maturity
        ytm: Yield to maturity (decimal)
    """
    try:
        data = request.get_json()
        
        bond = Bond(
            id="calc-bond",
            name="Duration Calc",
            par_value=data.get('par_value', 1000),
            coupon_rate=data.get('coupon_rate', 0.05),
            maturity_years=data.get('maturity_years', 5),
            ytm=data.get('ytm', 0.05)
        )
        
        metrics = await _service.calculate_duration(bond)
        
        return jsonify({
            "success": True,
            "data": {
                "macaulay_duration": metrics.macaulay_duration,
                "modified_duration": metrics.modified_duration,
                "convexity": metrics.convexity,
                "dollar_duration": metrics.dollar_duration
            }
        })
        
    except Exception as e:
        logger.error(f"Duration calculation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@fixed_income_bp.route('/wal', methods=['POST'])
async def calculate_wal():
    """
    Calculate Weighted Average Life for a bond ladder.
    
    Request Body:
        bonds: List of {par_value, maturity_years}
    """
    try:
        data = request.get_json()
        bonds_data = data.get('bonds', [])
        
        bonds = [
            Bond(
                id=f"bond-{i}",
                name=f"Bond {i}",
                par_value=b.get('par_value', 1000),
                coupon_rate=0.05,
                maturity_years=b.get('maturity_years', 5)
            )
            for i, b in enumerate(bonds_data)
        ]
        
        wal = await _service.calculate_weighted_average_life(bonds)
        
        return jsonify({
            "success": True,
            "data": {
                "weighted_average_life": wal,
                "bond_count": len(bonds)
            }
        })
        
    except Exception as e:
        logger.error(f"WAL calculation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@fixed_income_bp.route('/gaps/<portfolio_id>', methods=['GET'])
async def get_liquidity_gaps(portfolio_id: str):
    """Get liquidity gap analysis for a bond ladder."""
    try:
        bonds = _service._get_mock_portfolio(portfolio_id)
        gaps = await _service.get_liquidity_gap_analysis(bonds)
        
        return jsonify({
            "success": True,
            "data": [
                {
                    "year": g.year,
                    "severity": g.severity,
                    "recommended_action": g.recommended_action
                }
                for g in gaps
            ]
        })
        
    except Exception as e:
        logger.error(f"Gap analysis failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@fixed_income_bp.route('/inversion', methods=['GET'])
async def check_inversion():
    """Check if yield curve is currently inverted."""
    try:
        is_inverted = await _service.detect_inversion()
        curve = await _service.get_yield_curve()
        
        spread = curve.rates.get("10Y", 0) - curve.rates.get("2Y", 0)
        
        return jsonify({
            "success": True,
            "data": {
                "is_inverted": is_inverted,
                "spread_10y_2y": round(spread, 2),
                "recession_signal": is_inverted
            }
        })
        
    except Exception as e:
        logger.error(f"Inversion check failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
