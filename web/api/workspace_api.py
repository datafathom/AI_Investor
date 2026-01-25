
from flask import Blueprint, jsonify, request, g
from services.workspace.user_preferences_service import get_user_preferences_service, WorkspaceLayout
from web.auth_utils import login_required

workspace_bp = Blueprint('workspace_api', __name__, url_prefix='/api/v1/user')

@workspace_bp.route('/workspace', methods=['GET'])
@login_required
def get_user_workspace():
    """Retrieve user workspace layout."""
    user_id = getattr(g, 'user_id', None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    name = request.args.get('name')
    service = get_user_preferences_service()
    workspace = service.get_workspace(user_id, name)
    
    if workspace:
        return jsonify(workspace.model_dump(by_alias=True)), 200
    return jsonify({"error": "Workspace not found"}), 404

@workspace_bp.route('/workspace', methods=['POST'])
@login_required
def save_user_workspace():
    """Save user workspace layout."""
    user_id = getattr(g, 'user_id', None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing layout data"}), 400
        
    try:
        workspace = WorkspaceLayout(**data)
        is_default = data.get('is_default', False)
        
        service = get_user_preferences_service()
        ws_id = service.save_workspace(user_id, workspace, is_default)
        
        return jsonify({"message": "Workspace saved", "id": ws_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@workspace_bp.route('/workspaces', methods=['GET'])
@login_required
def list_user_workspaces():
    """List all workspaces for user."""
    user_id = getattr(g, 'user_id', None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    service = get_user_preferences_service()
    workspaces = service.list_workspaces(user_id)
    return jsonify(workspaces), 200
