
from flask import Blueprint, jsonify, request, g
from services.portfolio.homeostasis_service import homeostasis_service
from services.execution.philanthropy_service import philanthropy_service

homeostasis_api = Blueprint('homeostasis_api', __name__)

@homeostasis_api.route('/status', methods=['GET'])
def get_status():
    tenant_id = g.get('tenant_id', 'default')
    status = homeostasis_service.get_homeostasis_status(tenant_id)
    return jsonify(status)

@homeostasis_api.route('/update', methods=['POST'])
def update_metrics():
    tenant_id = g.get('tenant_id', 'default')
    data = request.json
    net_worth = data.get('net_worth')
    
    if net_worth is not None:
        homeostasis_service.update_net_worth(tenant_id, net_worth)
        
    status = homeostasis_service.get_homeostasis_status(tenant_id)
    return jsonify(status)

@homeostasis_api.route('/donate', methods=['POST'])
def manual_donate():
    tenant_id = g.get('tenant_id', 'default')
    data = request.json
    amount = data.get('amount', 0)
    
    philanthropy_service.donate_excess_alpha(tenant_id, amount)
    return jsonify({"status": "success", "amount": amount})
