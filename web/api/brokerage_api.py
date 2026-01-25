from flask import Blueprint, jsonify, request, g
from services.brokerage.brokerage_service import get_brokerage_service
from web.auth_utils import login_required, requires_role
import logging

logger = logging.getLogger(__name__)
brokerage_bp = Blueprint('brokerage_api', __name__, url_prefix='/api/v1/brokerage')

@brokerage_bp.route('/status', methods=['GET'])
@login_required
def get_brokerage_status():
    """Returns the current connection status and account summary."""
    try:
        service = get_brokerage_service()
        return jsonify(service.get_status())
    except Exception as e:
        logger.error(f"Error getting brokerage status: {e}")
        return jsonify({"error": "Failed to fetch status"}), 500

@brokerage_bp.route('/providers', methods=['GET'])
@login_required
def get_supported_providers():
    """Returns the list of supported brokerage/vendor integrations."""
    try:
        service = get_brokerage_service()
        return jsonify(service.get_supported_providers())
    except Exception as e:
        logger.error(f"Error getting providers: {e}")
        return jsonify({"error": "Failed to fetch providers"}), 500

@brokerage_bp.route('/positions', methods=['GET'])
@login_required
def get_brokerage_positions():
    """Fetches all open positions from the connected broker."""
    try:
        service = get_brokerage_service()
        return jsonify(service.get_positions())
    except Exception as e:
        logger.error(f"Error getting brokerage positions: {e}")
        return jsonify({"error": "Failed to fetch positions"}), 500

@brokerage_bp.route('/connect', methods=['POST'])
@login_required
@requires_role('trader')
def connect_brokerage():
    """Updates/Validates brokerage API credentials."""
    data = request.json or {}
    api_key = data.get('api_key')
    secret_key = data.get('secret_key')
    base_url = data.get('base_url')
    
    if not api_key or not secret_key:
        return jsonify({"error": "Missing credentials"}), 400
        
    try:
        service = get_brokerage_service()
        success = service.connect_with_keys(api_key, secret_key, base_url)
        if success:
            return jsonify({"status": "success", "message": "Brokerage connected successfully"})
        else:
            return jsonify({"status": "error", "message": "Invalid credentials or connection failure"}), 401
    except Exception as e:
        logger.error(f"Error connecting to brokerage: {e}")
        return jsonify({"error": str(e)}), 500
