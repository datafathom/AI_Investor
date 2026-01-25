"""
==============================================================================
FILE: web/api/retirement_api.py
ROLE: Retirement Planning API Endpoints
PURPOSE: REST endpoints for retirement projections and withdrawal strategies.

INTEGRATION POINTS:
    - RetirementProjectionService: Retirement projections
    - WithdrawalStrategyService: Withdrawal optimization
    - FrontendRetirement: Retirement dashboard widgets

ENDPOINTS:
    - POST /api/retirement/project
    - POST /api/retirement/compare
    - POST /api/retirement/withdrawal/plan
    - GET /api/retirement/rmd/:user_id
    - POST /api/retirement/withdrawal/optimize

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.retirement.retirement_projection_service import get_retirement_projection_service
from services.retirement.withdrawal_strategy_service import get_withdrawal_strategy_service
from models.retirement import RetirementScenario

logger = logging.getLogger(__name__)

retirement_bp = Blueprint('retirement', __name__, url_prefix='/api/retirement')


@retirement_bp.route('/project', methods=['POST'])
async def project_retirement():
    """
    Project retirement with Monte Carlo simulation.
    
    Request body:
        scenario: RetirementScenario object
        n_simulations: Number of simulations (default: 10000)
    """
    try:
        data = request.get_json() or {}
        scenario_data = data.get('scenario')
        n_simulations = int(data.get('n_simulations', 10000))
        
        if not scenario_data:
            return jsonify({
                'success': False,
                'error': 'scenario is required'
            }), 400
        
        scenario = RetirementScenario(**scenario_data)
        
        service = get_retirement_projection_service()
        projection = await service.project_retirement(scenario, n_simulations)
        
        return jsonify({
            'success': True,
            'data': projection.dict()
        })
        
    except Exception as e:
        logger.error(f"Error projecting retirement: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@retirement_bp.route('/compare', methods=['POST'])
async def compare_scenarios():
    """
    Compare multiple retirement scenarios.
    
    Request body:
        scenarios: List of RetirementScenario objects
        n_simulations: Number of simulations per scenario
    """
    try:
        data = request.get_json() or {}
        scenarios_data = data.get('scenarios', [])
        n_simulations = int(data.get('n_simulations', 10000))
        
        if not scenarios_data:
            return jsonify({
                'success': False,
                'error': 'scenarios are required'
            }), 400
        
        scenarios = [RetirementScenario(**s) for s in scenarios_data]
        
        service = get_retirement_projection_service()
        results = await service.compare_scenarios(scenarios, n_simulations)
        
        return jsonify({
            'success': True,
            'data': {name: proj.dict() for name, proj in results.items()}
        })
        
    except Exception as e:
        logger.error(f"Error comparing scenarios: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@retirement_bp.route('/withdrawal/plan', methods=['POST'])
async def create_withdrawal_plan():
    """
    Create withdrawal plan.
    
    Request body:
        user_id: User identifier
        strategy: Withdrawal strategy type
        initial_withdrawal_amount: Initial annual withdrawal
        withdrawal_rate: Optional withdrawal rate
        inflation_adjustment: Whether to adjust for inflation
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        strategy = data.get('strategy', 'inflation_adjusted')
        initial_withdrawal_amount = float(data.get('initial_withdrawal_amount', 0))
        withdrawal_rate = data.get('withdrawal_rate')
        inflation_adjustment = data.get('inflation_adjustment', True)
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        service = get_withdrawal_strategy_service()
        plan = await service.create_withdrawal_plan(
            user_id=user_id,
            strategy=strategy,
            initial_withdrawal_amount=initial_withdrawal_amount,
            withdrawal_rate=withdrawal_rate,
            inflation_adjustment=inflation_adjustment
        )
        
        return jsonify({
            'success': True,
            'data': plan.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating withdrawal plan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@retirement_bp.route('/rmd/<user_id>', methods=['GET'])
async def get_rmds(user_id: str):
    """
    Get RMD calculations for user.
    """
    try:
        service = get_withdrawal_strategy_service()
        accounts = await service._get_account_balances(user_id)
        rmds = await service._calculate_rmds(user_id, accounts)
        
        return jsonify({
            'success': True,
            'data': rmds or {}
        })
        
    except Exception as e:
        logger.error(f"Error calculating RMDs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@retirement_bp.route('/withdrawal/optimize', methods=['POST'])
async def optimize_withdrawal_rate():
    """
    Optimize withdrawal rate.
    
    Request body:
        retirement_savings: Total retirement savings
        annual_expenses: Annual expenses
        years_in_retirement: Expected years in retirement
        expected_return: Expected annual return
    """
    try:
        data = request.get_json() or {}
        retirement_savings = float(data.get('retirement_savings', 0))
        annual_expenses = float(data.get('annual_expenses', 0))
        years_in_retirement = int(data.get('years_in_retirement', 30))
        expected_return = float(data.get('expected_return', 0.06))
        
        service = get_withdrawal_strategy_service()
        result = await service.optimize_withdrawal_rate(
            retirement_savings=retirement_savings,
            annual_expenses=annual_expenses,
            years_in_retirement=years_in_retirement,
            expected_return=expected_return
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Error optimizing withdrawal rate: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
