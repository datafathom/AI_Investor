
from flask import Blueprint, jsonify, request, Response
from services.system.privacy_service import get_privacy_service
from web.auth_utils import login_required
from flask import g
import json

privacy_bp = Blueprint('privacy_api', __name__, url_prefix='/api/v1/privacy')

@privacy_bp.route('/export', methods=['GET'])
@login_required
def export_data():
    """
    Trigger a GDPR data export for the authenticated user.
    """
    user_id = getattr(g, 'user_id', None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    service = get_privacy_service()
    try:
        data = service.export_user_data(user_id)
        return Response(
            json.dumps(data, indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=my_data.json'}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@privacy_bp.route('/forget-me', methods=['DELETE'])
@login_required
def delete_account():
    """
    Trigger the 'Right to be Forgotten' for the authenticated user.
    """
    user_id = getattr(g, 'user_id', None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    service = get_privacy_service()
    success = service.delete_user_account(user_id)
    if success:
        return jsonify({"message": "Account and data deleted successfully"}), 200
    return jsonify({"error": "Failed to delete account"}), 500
