"""
==============================================================================
FILE: web/api/tax_optimization_api.py
ROLE: Tax Optimization API Endpoints
PURPOSE: REST endpoints for tax-loss harvesting and tax optimization.

INTEGRATION POINTS:
    - EnhancedTaxHarvestingService: Harvest opportunity identification
    - TaxOptimizationService: Tax optimization calculations
    - FrontendTax: Tax dashboard widgets

ENDPOINTS:
    - GET /api/tax/harvest/opportunities/:portfolio_id
    - POST /api/tax/harvest/batch/:portfolio_id
    - POST /api/tax/harvest/execute/:portfolio_id
    - POST /api/tax/optimize/lot_selection/:portfolio_id
    - POST /api/tax/optimize/project/:portfolio_id
    - POST /api/tax/optimize/withdrawal/:portfolio_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.tax.enhanced_tax_harvesting_service import get_enhanced_harvest_service
from services.tax.tax_optimization_service import get_tax_optimization_service

logger = logging.getLogger(__name__)

tax_optimization_bp = Blueprint('tax_optimization', __name__, url_prefix='/api/tax')


@tax_optimization_bp.route('/harvest/opportunities/<portfolio_id>', methods=['GET'])
async def get_harvest_opportunities(portfolio_id: str):
    """
    Get tax-loss harvesting opportunities.
    
    Query params:
        min_loss_dollar: Minimum loss in dollars (default: 500)
        min_loss_pct: Minimum loss percentage (default: 0.05)
    """
    try:
        min_loss_dollar = float(request.args.get('min_loss_dollar', 500))
        min_loss_pct = float(request.args.get('min_loss_pct', 0.05))
        
        service = get_enhanced_harvest_service()
        opportunities = await service.identify_harvest_opportunities(
            portfolio_id=portfolio_id,
            min_loss_dollar=min_loss_dollar,
            min_loss_pct=min_loss_pct
        )
        
        return jsonify({
            'success': True,
            'data': [
                {
                    'candidate': {
                        'ticker': opp.candidate.ticker,
                        'unrealized_loss': opp.candidate.unrealized_loss,
                        'cost_basis': opp.candidate.cost_basis,
                        'current_value': opp.candidate.current_value
                    },
                    'tax_savings': opp.tax_savings,
                    'net_benefit': opp.net_benefit,
                    'replacement_suggestions': opp.replacement_suggestions,
                    'wash_sale_risk': opp.wash_sale_risk,
                    'rank': opp.rank
                }
                for opp in opportunities
            ]
        })
        
    except Exception as e:
        logger.error(f"Error getting harvest opportunities: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tax_optimization_bp.route('/harvest/batch/<portfolio_id>', methods=['POST'])
async def analyze_batch_harvest(portfolio_id: str):
    """
    Analyze batch harvesting opportunities.
    
    Request body:
        opportunities: Optional pre-identified opportunities
    """
    try:
        data = request.get_json() or {}
        opportunities_data = data.get('opportunities')
        
        service = get_enhanced_harvest_service()
        result = await service.batch_harvest_analysis(
            portfolio_id=portfolio_id,
            opportunities=opportunities_data
        )
        
        return jsonify({
            'success': True,
            'data': {
                'total_tax_savings': result.total_tax_savings,
                'total_net_benefit': result.total_net_benefit,
                'trades_required': result.trades_required,
                'requires_approval': result.requires_approval,
                'opportunities': [
                    {
                        'candidate': {
                            'ticker': opp.candidate.ticker,
                            'unrealized_loss': opp.candidate.unrealized_loss
                        },
                        'tax_savings': opp.tax_savings,
                        'net_benefit': opp.net_benefit,
                        'rank': opp.rank
                    }
                    for opp in result.opportunities
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Error analyzing batch harvest: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tax_optimization_bp.route('/harvest/execute/<portfolio_id>', methods=['POST'])
async def execute_harvest(portfolio_id: str):
    """
    Execute tax-loss harvest trade.
    
    Request body:
        opportunity: EnhancedHarvestOpportunity object
        replacement_symbol: Optional replacement symbol
        approved: Whether user has approved
    """
    try:
        data = request.get_json() or {}
        opportunity_data = data.get('opportunity')
        replacement_symbol = data.get('replacement_symbol')
        approved = data.get('approved', False)
        
        if not opportunity_data:
            return jsonify({
                'success': False,
                'error': 'opportunity is required'
            }), 400
        
        from services.tax.enhanced_tax_harvesting_service import EnhancedHarvestOpportunity
        from services.tax.harvest_service import HarvestCandidate
        
        candidate = HarvestCandidate(**opportunity_data['candidate'])
        opportunity = EnhancedHarvestOpportunity(
            candidate=candidate,
            tax_savings=opportunity_data.get('tax_savings', 0.0),
            net_benefit=opportunity_data.get('net_benefit', 0.0),
            replacement_suggestions=opportunity_data.get('replacement_suggestions', []),
            wash_sale_risk=opportunity_data.get('wash_sale_risk', False),
            rank=opportunity_data.get('rank', 0)
        )
        
        service = get_enhanced_harvest_service()
        result = await service.execute_harvest(
            portfolio_id=portfolio_id,
            opportunity=opportunity,
            replacement_symbol=replacement_symbol,
            approved=approved
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Error executing harvest: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tax_optimization_bp.route('/optimize/lot_selection/<portfolio_id>', methods=['POST'])
async def optimize_lot_selection(portfolio_id: str):
    """
    Optimize lot selection for tax efficiency.
    
    Request body:
        symbol: Symbol to sell
        quantity: Quantity to sell
        method: Lot selection method (fifo, lifo, highest_cost, lowest_cost)
    """
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol')
        quantity = float(data.get('quantity', 0))
        method = data.get('method', 'highest_cost')
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'symbol is required'
            }), 400
        
        service = get_tax_optimization_service()
        result = await service.optimize_lot_selection(
            portfolio_id=portfolio_id,
            symbol=symbol,
            quantity=quantity,
            method=method
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Error optimizing lot selection: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tax_optimization_bp.route('/optimize/project/<portfolio_id>', methods=['POST'])
async def project_tax(portfolio_id: str):
    """
    Project year-end tax liability.
    
    Request body:
        planned_transactions: Optional list of planned transactions
    """
    try:
        data = request.get_json() or {}
        planned_transactions = data.get('planned_transactions')
        
        service = get_tax_optimization_service()
        projection = await service.project_year_end_tax(
            portfolio_id=portfolio_id,
            planned_transactions=planned_transactions
        )
        
        return jsonify({
            'success': True,
            'data': projection
        })
        
    except Exception as e:
        logger.error(f"Error projecting tax: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tax_optimization_bp.route('/optimize/withdrawal/<portfolio_id>', methods=['POST'])
async def optimize_withdrawal(portfolio_id: str):
    """
    Optimize withdrawal sequence for tax efficiency.
    
    Request body:
        withdrawal_amount: Total amount to withdraw
        account_types: Available account types
    """
    try:
        data = request.get_json() or {}
        withdrawal_amount = float(data.get('withdrawal_amount', 0))
        account_types = data.get('account_types', ['taxable', 'tax_deferred', 'tax_free'])
        
        service = get_tax_optimization_service()
        result = await service.optimize_withdrawal_sequence(
            portfolio_id=portfolio_id,
            withdrawal_amount=withdrawal_amount,
            account_types=account_types
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Error optimizing withdrawal: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
