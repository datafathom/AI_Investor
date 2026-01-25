"""
==============================================================================
FILE: web/api/estate_api.py
ROLE: Estate Planning API Endpoints
PURPOSE: REST endpoints for estate planning and inheritance simulation.

INTEGRATION POINTS:
    - EstatePlanningService: Estate plan management
    - InheritanceSimulator: Inheritance projections
    - FrontendEstate: Estate dashboard widgets

ENDPOINTS:
    - POST /api/estate/plan/create
    - GET /api/estate/plan/:user_id
    - PUT /api/estate/plan/:plan_id/beneficiary/:beneficiary_id
    - POST /api/estate/tax/calculate
    - POST /api/estate/inheritance/simulate/:plan_id
    - POST /api/estate/inheritance/compare

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.estate.estate_planning_service import get_estate_planning_service
from services.estate.inheritance_simulator import get_inheritance_simulator
from models.estate import EstateScenario

logger = logging.getLogger(__name__)

estate_bp = Blueprint('estate', __name__, url_prefix='/api/estate')


@estate_bp.route('/plan/create', methods=['POST'])
async def create_estate_plan():
    """
    Create estate plan.
    
    Request body:
        user_id: User identifier
        beneficiaries: List of beneficiary objects
        trust_accounts: Optional trust account information
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        beneficiaries = data.get('beneficiaries', [])
        trust_accounts = data.get('trust_accounts')
        
        if not user_id or not beneficiaries:
            return jsonify({
                'success': False,
                'error': 'user_id and beneficiaries are required'
            }), 400
        
        service = get_estate_planning_service()
        plan = await service.create_estate_plan(
            user_id=user_id,
            beneficiaries=beneficiaries,
            trust_accounts=trust_accounts
        )
        
        return jsonify({
            'success': True,
            'data': plan.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating estate plan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@estate_bp.route('/plan/<user_id>', methods=['GET'])
async def get_estate_plan(user_id: str):
    """
    Get estate plan for user.
    """
    try:
        from services.system.cache_service import get_cache_service
        cache_service = get_cache_service()
        plan_data = cache_service.get(f"estate_plan:{user_id}")
        
        if not plan_data:
            return jsonify({
                'success': False,
                'error': 'Estate plan not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': plan_data
        })
        
    except Exception as e:
        logger.error(f"Error getting estate plan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@estate_bp.route('/plan/<plan_id>/beneficiary/<beneficiary_id>', methods=['PUT'])
async def update_beneficiary(plan_id: str, beneficiary_id: str):
    """
    Update beneficiary in estate plan.
    
    Request body:
        updates: Dictionary of updates to apply
    """
    try:
        data = request.get_json() or {}
        updates = data.get('updates', {})
        
        service = get_estate_planning_service()
        beneficiary = await service.update_beneficiary(
            plan_id=plan_id,
            beneficiary_id=beneficiary_id,
            updates=updates
        )
        
        return jsonify({
            'success': True,
            'data': beneficiary.dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating beneficiary: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@estate_bp.route('/tax/calculate', methods=['POST'])
async def calculate_estate_tax():
    """
    Calculate estate tax.
    
    Request body:
        estate_value: Total estate value
        exemptions: Optional exemption amount
    """
    try:
        data = request.get_json() or {}
        estate_value = float(data.get('estate_value', 0))
        exemptions = data.get('exemptions')
        
        service = get_estate_planning_service()
        tax_calc = await service.calculate_estate_tax(
            estate_value=estate_value,
            exemptions=exemptions
        )
        
        return jsonify({
            'success': True,
            'data': tax_calc
        })
        
    except Exception as e:
        logger.error(f"Error calculating estate tax: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@estate_bp.route('/inheritance/simulate/<plan_id>', methods=['POST'])
async def simulate_inheritance(plan_id: str):
    """
    Simulate inheritance for estate plan.
    
    Request body:
        projection_years: Years to project forward (default: 10)
    """
    try:
        data = request.get_json() or {}
        projection_years = int(data.get('projection_years', 10))
        
        simulator = get_inheritance_simulator()
        projections = await simulator.simulate_inheritance(
            plan_id=plan_id,
            projection_years=projection_years
        )
        
        return jsonify({
            'success': True,
            'data': [p.dict() for p in projections]
        })
        
    except Exception as e:
        logger.error(f"Error simulating inheritance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@estate_bp.route('/inheritance/compare', methods=['POST'])
async def compare_inheritance_scenarios():
    """
    Compare inheritance scenarios.
    
    Request body:
        scenarios: List of EstateScenario objects
    """
    try:
        data = request.get_json() or {}
        scenarios_data = data.get('scenarios', [])
        
        if not scenarios_data:
            return jsonify({
                'success': False,
                'error': 'scenarios are required'
            }), 400
        
        scenarios = [EstateScenario(**s) for s in scenarios_data]
        
        simulator = get_inheritance_simulator()
        results = await simulator.compare_scenarios(scenarios)
        
        return jsonify({
            'success': True,
            'data': {
                name: [p.dict() for p in projections]
                for name, projections in results.items()
            }
        })
        
    except Exception as e:
        logger.error(f"Error comparing scenarios: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
