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
from services.strategy.dynamic_allocator import get_dynamic_allocator
from services.risk.risk_monitor import get_risk_monitor
from services.risk.circuit_breaker import get_circuit_breaker
from services.execution.paper_exchange import get_paper_exchange

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/v1/dashboard')

@dashboard_bp.route('/allocation', methods=['GET'])
def get_allocation():
    """
    Get current target allocation based on Fear Index.
    Query Param: fear_index (default 50)
    """
    fear_index = float(request.args.get('fear_index', 50.0))
    allocator = get_dynamic_allocator()
    
    # High Level Buckets
    buckets = allocator.allocate_capital(fear_index)
    
    # Detailed Portfolio (Mock Assets for now)
    # in real usage, we'd pass real available assets
    import pandas as pd
    import numpy as np
    mock_assets = {
        'SPY': pd.DataFrame({'close': [400.0]}),
        'TLT': pd.DataFrame({'close': [100.0]})
    }
    targets = allocator.construct_target_portfolio(mock_assets, fear_index)
    
    return jsonify({
        "fear_index": fear_index,
        "buckets": buckets,
        "target_weights": targets
    })

@dashboard_bp.route('/risk', methods=['GET'])
def get_risk_status():
    """
    Get Risk Metrics.
    """
    monitor = get_risk_monitor()
    breaker = get_circuit_breaker()
    
    # Mock Portfolio for VaR
    # In reality, fetch from Execution Service
    exchange = get_paper_exchange()
    summary = exchange.get_account_summary()
    cash = summary['cash'] # total_value approx
    
    # Calculate VaR
    var_95 = monitor.calculate_parametric_var(cash, 0.02) # 2% daily vol assumption
    
    # Circuit Breaker Status
    return jsonify({
        "var_95_daily": var_95,
        "portfolio_frozen": breaker.portfolio_frozen,
        "freeze_reason": breaker.freeze_reason,
        "frozen_assets": list(breaker.frozen_assets)
    })

@dashboard_bp.route('/execution', methods=['GET'])
def get_execution_status():
    """
    Get Paper Trading Account Status.
    """
    exchange = get_paper_exchange()
    summary = exchange.get_account_summary()
    
    return jsonify({
        "balance": summary["cash"],
        "positions": summary["positions"]
    })
