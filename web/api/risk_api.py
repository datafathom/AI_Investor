from flask import Blueprint, request, jsonify
from services.risk.risk_monitor import get_risk_monitor
from services.risk.circuit_breaker import get_circuit_breaker
import logging

logger = logging.getLogger(__name__)
risk_bp = Blueprint('risk_api', __name__)

@risk_bp.route('/status', methods=['GET'])
def get_risk_status():
    """Get current exposure and limit status."""
    monitor = get_risk_monitor()
    breaker = get_circuit_breaker()
    sentiment_multiplier = monitor.calculate_sentiment_multiplier()
    
    from services.analysis.fear_greed_service import get_fear_greed_service
    fg_data = get_fear_greed_service(mock=True).get_fear_greed_index()
    
    return jsonify({
        "halted": breaker.is_halted(),
        "freeze_reason": breaker.freeze_reason,
        "sentiment": {
            "score": fg_data['score'],
            "label": fg_data['label'],
            "multiplier": sentiment_multiplier
        },
        "limits": {
            "max_pos": monitor.MAX_POSITION_SIZE_USD,
            "scaled_max_pos": monitor.MAX_POSITION_SIZE_USD * sentiment_multiplier,
            "max_loss": monitor.MAX_DAILY_LOSS_USD
        }
    })

@risk_bp.route('/kill-switch', methods=['POST'])
def toggle_kill_switch():
    """Emergency halt / Global Kill Switch."""
    data = request.json or {}
    action = data.get('action') # 'engage' or 'reset'
    reason = data.get('reason', 'Manual emergency trigger')
    
    breaker = get_circuit_breaker()
    
    if action == 'engage':
        breaker.trigger_global_kill_switch(reason)
        return jsonify({"status": "HALTED", "reason": reason})
    elif action == 'reset':
        breaker.reset()
        return jsonify({"status": "NOMINAL"})
    
    return jsonify({"error": "Invalid action"}), 400

@risk_bp.route('/preview', methods=['POST'])
def risk_preview():
    """AI-assisted trade risk analysis."""
    data = request.json
    if not data or not all(k in data for k in ('symbol', 'side', 'quantity', 'price')):
        return jsonify({"error": "Missing trade details"}), 400
        
    monitor = get_risk_monitor()
    analysis = monitor.analyze_trade_risk(
        symbol=data['symbol'],
        side=data['side'],
        quantity=float(data['quantity']),
        price=float(data['price'])
    )
    
    return jsonify(analysis)
