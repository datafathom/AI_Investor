"""
Attribution API - REST endpoints for portfolio performance attribution.

This blueprint provides endpoints for accessing Brinson-Fachler attribution
analysis, enabling frontend widgets to display sector-level performance
decomposition and regime shift detection.

Endpoints:
    GET  /api/v1/attribution/<portfolio_id>     - Full attribution analysis
    GET  /api/v1/attribution/benchmarks         - Available benchmarks
    POST /api/v1/attribution/compare            - Multi-benchmark comparison
"""

from flask import Blueprint, jsonify, request
from services.analysis.attribution_service import (
    AttributionService,
    DateRange
)
import logging

logger = logging.getLogger(__name__)

attribution_bp = Blueprint('attribution', __name__)
_service = AttributionService()


@attribution_bp.route('/<portfolio_id>', methods=['GET'])
async def get_attribution(portfolio_id: str):
    """
    Get full Brinson-Fachler attribution for a portfolio.
    
    Query Params:
        benchmark: Benchmark ID (default: sp500)
        start: Start date for analysis period
        end: End date for analysis period
        
    Returns:
        JSON with complete attribution breakdown
    """
    try:
        benchmark_id = request.args.get('benchmark', 'sp500')
        start_date = request.args.get('start', '2025-01-01')
        end_date = request.args.get('end', '2025-12-31')
        
        result = await _service.calculate_brinson_attribution(
            portfolio_id=portfolio_id,
            benchmark_id=benchmark_id,
            period=DateRange(start=start_date, end=end_date)
        )
        
        # Convert dataclass to dict for JSON serialization
        return jsonify({
            "success": True,
            "data": {
                "portfolio_id": result.portfolio_id,
                "benchmark_id": result.benchmark_id,
                "period": {
                    "start": result.period.start,
                    "end": result.period.end
                },
                "total_active_return": result.total_active_return,
                "total_allocation_effect": result.total_allocation_effect,
                "total_selection_effect": result.total_selection_effect,
                "total_interaction_effect": result.total_interaction_effect,
                "sector_attributions": [
                    {
                        "sector": sa.sector,
                        "allocation_effect": sa.allocation_effect,
                        "selection_effect": sa.selection_effect,
                        "interaction_effect": sa.interaction_effect,
                        "portfolio_weight": sa.portfolio_weight,
                        "benchmark_weight": sa.benchmark_weight,
                        "portfolio_return": sa.portfolio_return,
                        "benchmark_return": sa.benchmark_return
                    }
                    for sa in result.sector_attributions
                ],
                "regime_shifts": [
                    {
                        "start_date": rs.start_date,
                        "end_date": rs.end_date,
                        "correlation_before": rs.correlation_before,
                        "correlation_during": rs.correlation_during,
                        "impact_basis_points": rs.impact_basis_points,
                        "description": rs.description
                    }
                    for rs in result.regime_shifts
                ],
                "calculated_at": result.calculated_at
            }
        })
        
    except Exception as e:
        logger.error(f"Attribution calculation failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@attribution_bp.route('/benchmarks', methods=['GET'])
def get_benchmarks():
    """Get list of available benchmarks for attribution comparison."""
    benchmarks = _service.get_available_benchmarks()
    return jsonify({
        "success": True,
        "data": benchmarks
    })


@attribution_bp.route('/compare', methods=['POST'])
async def compare_benchmarks():
    """
    Compare portfolio attribution against multiple benchmarks.
    
    Request Body:
        portfolio_id: Portfolio to analyze
        benchmarks: List of benchmark IDs to compare
        period: { start, end } date range
        
    Returns:
        Attribution results for each benchmark
    """
    try:
        data = request.get_json()
        portfolio_id = data.get('portfolio_id')
        benchmark_ids = data.get('benchmarks', ['sp500', 'nasdaq'])
        period_data = data.get('period', {'start': '2025-01-01', 'end': '2025-12-31'})
        
        period = DateRange(start=period_data['start'], end=period_data['end'])
        
        results = []
        for benchmark_id in benchmark_ids:
            result = await _service.calculate_brinson_attribution(
                portfolio_id=portfolio_id,
                benchmark_id=benchmark_id,
                period=period
            )
            results.append({
                "benchmark_id": benchmark_id,
                "total_active_return": result.total_active_return,
                "total_allocation_effect": result.total_allocation_effect,
                "total_selection_effect": result.total_selection_effect,
                "total_interaction_effect": result.total_interaction_effect
            })
        
        return jsonify({
            "success": True,
            "data": results
        })
        
    except Exception as e:
        logger.error(f"Benchmark comparison failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@attribution_bp.route('/sector/<portfolio_id>/<sector>', methods=['GET'])
async def get_sector_attribution(portfolio_id: str, sector: str):
    """
    Get attribution for a specific sector.
    
    Returns:
        Allocation, selection, and interaction effects for the sector
    """
    try:
        allocation = await _service.get_sector_allocation_effect(portfolio_id, sector)
        selection = await _service.get_selection_effect(portfolio_id, sector)
        
        return jsonify({
            "success": True,
            "data": {
                "sector": sector,
                "allocation_effect": allocation,
                "selection_effect": selection
            }
        })
        
    except Exception as e:
        logger.error(f"Sector attribution failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
