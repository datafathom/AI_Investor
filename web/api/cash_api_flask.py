"""
Cash API - multi-currency Management (Flask Version)
Phase 56: Endpoints for FX rates, balances, and sweep suggestions.
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.trading.fx_service import get_fx_service

cash_bp = Blueprint('cash_api', __name__)
logger = logging.getLogger(__name__)

@cash_bp.route('/dashboard', methods=['GET'])
def get_cash_dashboard():
    service = get_fx_service()
    data = asyncio.run(service.get_balances())
    rates = asyncio.run(service.get_fx_rates())
    total_usd = asyncio.run(service.get_total_value_usd())
    
    return jsonify({
        "balances": [
            {
                "currency": b.currency,
                "amount": b.amount,
                "usd_value": b.amount_usd,
                "allocation_pct": b.allocation_pct,
                "interest_rate": b.interest_rate
            } for b in data
        ],
        "fx_rates": {r.pair: {"rate": r.rate, "spread": r.spread} for r in rates},
        "total_value_usd": total_usd,
        "last_updated": rates[0].timestamp if rates else None
    })

@cash_bp.route('/fx/rates', methods=['GET'])
def get_fx_rates():
    service = get_fx_service()
    rates = asyncio.run(service.get_fx_rates())
    return jsonify({r.pair: r.rate for r in rates})

@cash_bp.route('/fx/convert', methods=['POST'])
def convert_currency():
    data = request.json
    from_curr = data.get('from_currency')
    to_curr = data.get('to_currency')
    amount = data.get('amount')
    
    if not all([from_curr, to_curr, amount]):
        return jsonify({"error": "Missing parameters"}), 400
        
    service = get_fx_service()
    result = asyncio.run(service.execute_conversion(from_curr, to_curr, amount))
    
    if not result.success:
        return jsonify({"success": False, "error": result.error_message}), 400
        
    return jsonify({
        "success": True,
        "rate": result.rate,
        "received": result.received_amount,
        "fee_usd": result.fee_usd
    })

@cash_bp.route('/sweep/suggestions', methods=['GET'])
def get_sweep_suggestions():
    service = get_fx_service()
    suggestions = asyncio.run(service.get_sweep_suggestions())
    return jsonify([
        {
            "id": s.id,
            "currency": s.currency,
            "amount": s.amount,
            "destination": s.destination,
            "estimated_yield": s.estimated_yield
        } for s in suggestions
    ])
