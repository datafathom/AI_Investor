"""
==============================================================================
FILE: web/api/advanced_risk_api.py
ROLE: Advanced Risk Management API Endpoints
PURPOSE: REST endpoints for advanced risk metrics and stress testing.

INTEGRATION POINTS:
    - AdvancedRiskMetricsService: Risk metrics calculations
    - StressTestingService: Stress test execution
    - FrontendRisk: Risk dashboard widgets

ENDPOINTS:
    - GET /api/risk/metrics/:portfolio_id
    - POST /api/risk/stress/historical/:portfolio_id
    - POST /api/risk/stress/monte_carlo/:portfolio_id
    - POST /api/risk/stress/custom/:portfolio_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.risk.advanced_risk_metrics_service import get_risk_metrics_service
from services.risk.stress_testing_service import get_stress_testing_service
from models.risk import StressScenario

logger = logging.getLogger(__name__)

advanced_risk_bp = Blueprint('advanced_risk', __name__, url_prefix='/api/risk')


@advanced_risk_bp.route('/metrics/<portfolio_id>', methods=['GET'])
async def get_risk_metrics(portfolio_id: str):
    """
    Get comprehensive risk metrics for portfolio.
    
    Query params:
        method: Calculation method (historical, parametric, monte_carlo)
        lookback_days: Lookback period in days (default: 252)
    """
    try:
        method = request.args.get('method', 'historical')
        lookback_days = int(request.args.get('lookback_days', 252))
        
        service = get_risk_metrics_service()
        metrics = await service.calculate_risk_metrics(
            portfolio_id=portfolio_id,
            method=method,
            lookback_days=lookback_days
        )
        
        return jsonify({
            'success': True,
            'data': metrics.dict()
        })
        
    except Exception as e:
        logger.error(f"Error calculating risk metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_risk_bp.route('/stress/historical/<portfolio_id>', methods=['POST'])
async def run_historical_stress(portfolio_id: str):
    """
    Run historical scenario stress test.
    
    Request body:
        scenario_name: Name of historical scenario (2008_financial_crisis, 2020_covid_crash, etc.)
    """
    try:
        data = request.get_json() or {}
        scenario_name = data.get('scenario_name')
        
        if not scenario_name:
            return jsonify({
                'success': False,
                'error': 'scenario_name is required'
            }), 400
        
        service = get_stress_testing_service()
        result = await service.run_historical_scenario(
            portfolio_id=portfolio_id,
            scenario_name=scenario_name
        )
        
        return jsonify({
            'success': True,
            'data': result.dict()
        })
        
    except Exception as e:
        logger.error(f"Error running historical stress test: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_risk_bp.route('/stress/monte_carlo/<portfolio_id>', methods=['POST'])
async def run_monte_carlo_stress(portfolio_id: str):
    """
    Run Monte Carlo stress test.
    
    Request body:
        n_simulations: Number of simulations (default: 10000)
        time_horizon_days: Time horizon in days (default: 252)
    """
    try:
        data = request.get_json() or {}
        n_simulations = int(data.get('n_simulations', 10000))
        time_horizon_days = int(data.get('time_horizon_days', 252))
        
        service = get_stress_testing_service()
        result = await service.run_monte_carlo_simulation(
            portfolio_id=portfolio_id,
            n_simulations=n_simulations,
            time_horizon_days=time_horizon_days
        )
        
        return jsonify({
            'success': True,
            'data': result.dict()
        })
        
    except Exception as e:
        logger.error(f"Error running Monte Carlo stress test: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@advanced_risk_bp.route('/stress/custom/<portfolio_id>', methods=['POST'])
async def run_custom_stress(portfolio_id: str):
    """
    Run custom stress scenario.
    
    Request body:
        scenario: StressScenario object
    """
    try:
        data = request.get_json() or {}
        scenario_data = data.get('scenario')
        
        if not scenario_data:
            return jsonify({
                'success': False,
                'error': 'scenario is required'
            }), 400
        
        scenario = StressScenario(**scenario_data)
        
        service = get_stress_testing_service()
        result = await service.run_custom_stress_scenario(
            portfolio_id=portfolio_id,
            scenario=scenario
        )
        
        return jsonify({
            'success': True,
            'data': result.dict()
        })
        
    except Exception as e:
        logger.error(f"Error running custom stress test: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
