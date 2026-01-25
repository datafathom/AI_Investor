
from flask import Blueprint, jsonify, request, g
from web.auth_utils import login_required, requires_role
from services.brokerage.settlement_service import get_settlement_service

settlement_bp = Blueprint('settlement_api_v1', __name__, url_prefix='/api/v1/settlement')

@settlement_bp.route('/balances', methods=['GET'])
@login_required
@requires_role('trader')
def get_balances():
    service = get_settlement_service()
    return jsonify(service.get_balance_summary())

@settlement_bp.route('/rates', methods=['GET'])
@login_required
def get_rates():
    from services.system.cache_service import get_cache_service
    cache = get_cache_service()
    
    cache_key = "settlement:rates"
    cached_rates = cache.get(cache_key)
    if cached_rates:
        return jsonify(cached_rates)

    service = get_settlement_service()
    rates = service.get_rates()
    
    # Cache for 60 seconds (Rates don't move that fast for simulated demo)
    cache.set(cache_key, rates, ttl=60)
    
    return jsonify(rates)

@settlement_bp.route('/convert', methods=['POST'])
@login_required
@requires_role('trader')
def convert_currency():
    data = request.json or {}
    from_curr = data.get('from')
    to_curr = data.get('to')
    amount = data.get('amount')
    
    if not from_curr or not to_curr or amount is None:
        return jsonify({"error": "Missing conversion parameters"}), 400
        
    service = get_settlement_service()
    result = service.convert_currency(from_curr, to_curr, float(amount))
    
    if result.get('status') == 'ERROR':
        return jsonify(result), 400
        
    return jsonify(result)
