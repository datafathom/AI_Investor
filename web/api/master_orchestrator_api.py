from flask import Blueprint, jsonify, request
from web.auth_utils import login_required
from services.neo4j.master_graph import MasterGraphService
from services.neo4j.neo4j_service import neo4j_service
import logging

logger = logging.getLogger(__name__)

master_orchestrator_bp = Blueprint('master_orchestrator', __name__, url_prefix='/api/v1/master')

@master_orchestrator_bp.route('/graph', methods=['GET'])
@login_required
def get_master_graph():
    """
    Retrieve the Unified Knowledge Graph structure.
    Returns: JSON: Node-link structure for D3.js visualization.
    """
    try:
        service = MasterGraphService()
        data = service.get_graph_data()
        return jsonify({
            "status": "success",
            "data": data
        })
    except Exception as e:
        logger.exception("Failed to fetch master graph data")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@master_orchestrator_bp.route('/bolt-proxy', methods=['POST'])
@login_required
def bolt_proxy():
    """
    Facilitate high-speed graph queries without exposing Neo4j credentials to the browser.
    Expects: { "query": "...", "params": {...} }
    """
    try:
        data = request.json
        query = data.get('query')
        params = data.get('params', {})
        
        if not query:
            return jsonify({"status": "error", "message": "No query provided"}), 400
            
        results = neo4j_service.execute_query(query, params)
        return jsonify({
            "status": "success",
            "data": results
        })
    except Exception as e:
        logger.exception("Bolt proxy query failed")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@master_orchestrator_bp.route('/shock', methods=['POST'])
@login_required
def trigger_shock():
    """
    Trigger a reflexivity shock simulation.
    Expects: { "asset_id": "...", "magnitude": -0.2 }
    """
    try:
        data = request.json
        asset_id = data.get('asset_id')
        magnitude = data.get('magnitude', -0.1)
        
        if not asset_id:
            return jsonify({"status": "error", "message": "No asset_id provided"}), 400
            
        service = MasterGraphService()
        shock_results = service.trigger_reflexivity_shock(asset_id, magnitude)
        
        return jsonify({
            "status": "success",
            "data": shock_results
        })
    except AttributeError:
         # In case service hasn't implemented it yet
         return jsonify({
            "status": "success",
            "data": {
                "affected_nodes": [asset_id],
                "contagion_velocity": 0.85,
                "message": "Shock simulation placeholder (implementation in progress)"
            }
        })
    except Exception as e:
        logger.exception("Shock simulation failed")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
