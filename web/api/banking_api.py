from flask import Blueprint, jsonify, request, g
from services.banking.banking_service import get_banking_service
from web.auth_utils import login_required, requires_role
import logging

logger = logging.getLogger(__name__)
banking_bp = Blueprint('banking_api', __name__, url_prefix='/api/v1/banking')

@banking_bp.route('/plaid/create-link-token', methods=['POST'])
@login_required
def create_link_token():
    """Initiates the Plaid Link flow by generating a link token."""
    try:
        service = get_banking_service()
        user_id = getattr(g, 'user_id', 'demo-user')
        token = service.create_link_token(user_id)
        return jsonify({"link_token": token})
    except Exception as e:
        logger.error(f"Error creating link token: {e}")
        return jsonify({"error": "Failed to initiate banking link"}), 500

@banking_bp.route('/plaid/exchange-public-token', methods=['POST'])
@login_required
def exchange_public_token():
    """Exchanges a public token from the frontend for a permanent access token."""
    data = request.get_json()
    public_token = data.get('public_token')
    
    if not public_token:
        return jsonify({"error": "Missing public token"}), 400
        
    try:
        service = get_banking_service()
        access_token = service.exchange_public_token(public_token)
        
        # In a real app, we'd save this access_token in the DB for the user
        logger.info(f"Successfully linked bank account for user {g.user_id}")
        
        return jsonify({"status": "success", "message": "Account linked successfully"})
    except Exception as e:
        logger.error(f"Error exchanging public token: {e}")
        return jsonify({"error": "Failed to link account"}), 500

@banking_bp.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    """Fetches all linked bank accounts and their balances."""
    try:
        service = get_banking_service()
        # In production, we'd fetch the user's access token from the DB first
        # For the demo, we use a dummy or let the service handle simulation
        accounts = service.get_accounts("DEMO_ACCESS_TOKEN")
        return jsonify(accounts)
    except Exception as e:
        logger.error(f"Error fetching accounts: {e}")
        return jsonify({"error": "Failed to fetch linked accounts"}), 500

@banking_bp.route('/sync', methods=['POST'])
@login_required
@requires_role('trader')
def sync_transactions():
    """Triggers a manual sync of banking transactions."""
    return jsonify({"status": "success", "message": "Transaction sync triggered"})

@banking_bp.route('/reconciliation', methods=['GET'])
@login_required
def get_reconciliation():
    """Fetches the latest reconciliation report."""
    try:
        from services.banking.reconciliation_service import get_reconciliation_service
        service = get_reconciliation_service()
        report = service.perform_reconciliation("DEMO_ACCESS_TOKEN")
        return jsonify(report)
    except Exception as e:
        logger.error(f"Error fetching reconciliation report: {e}")
        return jsonify({"error": "Failed to fetch reconciliation report"}), 500
