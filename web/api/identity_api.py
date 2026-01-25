from flask import Blueprint, jsonify, request, g
import logging
from services.system.identity_service import IdentityService
from web.auth_utils import login_required

identity_api = Blueprint('identity_api', __name__)
logger = logging.getLogger(__name__)

identity_service = IdentityService()

@identity_api.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """
    Get the current reconciled identity profile and trust score.
    """
    try:
        user_id = g.user_id
        profile = identity_service.get_identity_profile(user_id)
        return jsonify(profile), 200
    except Exception as e:
        logger.exception(f"Error fetching identity profile for {g.user_id}")
        return jsonify({'error': 'Failed to fetch identity profile'}), 500

@identity_api.route('/reconcile', methods=['POST'])
@login_required
def trigger_reconcile():
    """
    Manually trigger an identity reconciliation run.
    """
    try:
        user_id = g.user_id
        profile = identity_service.reconcile_identity(user_id)
        return jsonify({'message': 'Reconciliation complete', 'data': profile}), 200
    except Exception as e:
        logger.exception(f"Error reconciling identity for {g.user_id}")
        return jsonify({'error': 'Reconciliation failed'}), 500

@identity_api.route('/manual-verify', methods=['POST'])
@login_required
def manual_verify():
    """
    Stub for uploading verification documents.
    """
    return jsonify({'message': 'Manual verification submission received (Stub)'}), 200
