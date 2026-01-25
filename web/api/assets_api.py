
from flask import Blueprint, jsonify, request
from services.portfolio.assets_service import assets_service

assets_bp = Blueprint('assets_api', __name__)

@assets_bp.route('/', methods=['GET'])
def get_assets():
    """Get all assets."""
    assets = assets_service.get_all_assets()
    return jsonify(assets)

@assets_bp.route('/', methods=['POST'])
def create_asset():
    """Create a new asset."""
    data = request.json
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({'error': 'Missing required fields (name, value)'}), 400
    
    asset = assets_service.add_asset(data)
    return jsonify(asset), 201

@assets_bp.route('/<asset_id>', methods=['PUT'])
def update_asset(asset_id):
    """Update an existing asset."""
    data = request.json
    updated_asset = assets_service.update_asset(asset_id, data)
    
    if updated_asset:
        return jsonify(updated_asset)
    return jsonify({'error': 'Asset not found'}), 404

@assets_bp.route('/<asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    """Delete an asset."""
    success = assets_service.delete_asset(asset_id)
    if success:
        return jsonify({'message': 'Asset deleted'})
    return jsonify({'error': 'Asset not found'}), 404

@assets_bp.route('/valuation', methods=['GET'])
def get_valuation():
    """Get total valuation summary."""
    total = assets_service.get_total_valuation()
    return jsonify({'total_valuation': total, 'currency': 'USD'})
