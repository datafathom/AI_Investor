
from flask import Blueprint, jsonify, request, g
from web.auth_utils import login_required
from services.system.social_auth_service import get_social_auth_service

payment_transfer_bp = Blueprint('payment_transfer', __name__, url_prefix='/api/v1/payments')

@payment_transfer_bp.route('/linked-vendors', methods=['GET'])
@login_required
def get_linked_vendors():
    """Returns a list of financial vendors linked to the user's account."""
    social_service = get_social_auth_service()
    user_email = None
    
    # Extract email from user_id (mock storage lookup)
    for email, udata in social_service.users.items():
        if str(udata["id"]) == str(g.user_id):
            user_email = email
            break
            
    if not user_email:
        return jsonify({"error": "User profile not found"}), 404
        
    vendors = social_service.get_linked_finance_vendors(user_email)
    return jsonify({
        "user_id": g.user_id,
        "email": user_email,
        "linked_vendors": vendors
    })

@payment_transfer_bp.route('/transfer', methods=['POST'])
@login_required
def transfer_funds():
    """Initiates a fund transfer from a linked vendor."""
    data = request.get_json()
    vendor = data.get('vendor')
    amount = data.get('amount')
    direction = data.get('direction', 'deposit') # deposit or withdraw
    
    if not vendor or not amount:
        return jsonify({"error": "Vendor and amount are required"}), 400
        
    social_service = get_social_auth_service()
    user_email = None
    for email, udata in social_service.users.items():
        if str(udata["id"]) == str(g.user_id):
            user_email = email
            break
            
    if not user_email:
        return jsonify({"error": "User session invalid"}), 404
        
    result = social_service.transfer_funds(user_email, vendor, float(amount), direction)
    
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 400
