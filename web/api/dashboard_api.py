"""
==============================================================================
FILE: web/api/dashboard_api.py
ROLE: Mission Control Data Feed
PURPOSE:
    Expose Strategy, Risk, and Execution status to the Frontend.
    
    Endpoints:
    - /api/v1/dashboard/allocation: Current Target Allocation.
    - /api/v1/dashboard/risk: VaR, Alerts, Circuit Breaker Status.
    - /api/v1/dashboard/execution: Portfolio Balance, Positions.
    
ROADMAP: Phase 27 - Mission Control API
==============================================================================
"""

from flask import Blueprint, jsonify, request
from web.auth_utils import login_required, requires_role
from services.strategy.dynamic_allocator import get_dynamic_allocator
from services.risk.risk_monitor import get_risk_monitor
from services.risk.circuit_breaker import get_circuit_breaker
from services.execution.paper_exchange import get_paper_exchange

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/v1/dashboard')

@dashboard_bp.route('/allocation', methods=['GET'])
@login_required
def get_allocation():
    """
    Get current target allocation based on Fear Index.
    
    Returns target weights for core asset classes (Equity, Fixed Income, Crypto, Cash)
    based on the current dynamic fear-greed index.
    
    Args:
        fear_index (float): Current fear market sentiment (0-100). Defaults to 50.0.
        
    Returns:
        JSON: Standardized response containing allocation buckets and target weights.
        
    Security:
        Bearer JWT required.
    """
    try:
        fear_index = float(request.args.get('fear_index', 50.0))
        allocator = get_dynamic_allocator()
        
        # High Level Buckets
        buckets = allocator.allocate_capital(fear_index)
        
        # Detailed Portfolio (Mock Assets for now)
        import pandas as pd
        mock_assets = {
            'SPY': pd.DataFrame({'close': [400.0]}),
            'TLT': pd.DataFrame({'close': [100.0]})
        }
        targets = allocator.construct_target_portfolio(mock_assets, fear_index)
        
        return jsonify({
            "status": "success",
            "data": {
                "fear_index": fear_index,
                "buckets": buckets,
                "target_weights": targets
            }
        })
    except Exception as e:
        logger.exception("Failed to fetch allocation")
        return jsonify({"status": "error", "message": str(e)}), 500

@dashboard_bp.route('/risk', methods=['GET'])
@login_required
def get_risk_status():
    """
    Retrieve real-time Risk Metrics and Circuit Breaker status.
    
    Provides Value-at-Risk (VaR) calculations and the current operational status
    of the system-wide circuit breakers.
    
    Returns:
        JSON: Standardized response with VaR metrics and freeze status.
        
    Security:
        Bearer JWT required.
    """
    try:
        monitor = get_risk_monitor()
        breaker = get_circuit_breaker()
        
        # Mock Portfolio for VaR
        exchange = get_paper_exchange()
        summary = exchange.get_account_summary()
        cash = summary['cash']
        
        # Calculate VaR
        var_95 = monitor.calculate_parametric_var(cash, 0.02)
        
        return jsonify({
            "status": "success",
            "data": {
                "var_95_daily": var_95,
                "portfolio_frozen": breaker.portfolio_frozen,
                "freeze_reason": breaker.freeze_reason,
                "frozen_assets": list(breaker.frozen_assets)
            }
        })
    except Exception as e:
        logger.exception("Failed to fetch risk status")
        return jsonify({"status": "error", "message": str(e)}), 500

@dashboard_bp.route('/execution', methods=['GET'])
@login_required
def get_execution_status():
    """
    Fetch Paper Trading Account balance and current positions.
    
    Retrieves the live status of the paper exchange, including available cash 
    and detailed position breakdown.
    
    Returns:
        JSON: Standardized response with balance and positions.
        
    Security:
        Bearer JWT required.
    """
    try:
        exchange = get_paper_exchange()
        summary = exchange.get_account_summary()
        
        return jsonify({
            "status": "success",
            "data": {
                "balance": summary["cash"],
                "positions": summary["positions"]
            }
        })
    except Exception as e:
        logger.exception("Failed to fetch execution status")
        return jsonify({"status": "error", "message": str(e)}), 500
