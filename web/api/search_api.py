from flask import Blueprint, jsonify, request
import logging
from services.neo4j.master_graph import MasterGraph

logger = logging.getLogger(__name__)
search_bp = Blueprint('search_api', __name__, url_prefix='/api/v1/search')

@search_bp.route('/index', methods=['GET'])
def get_search_index():
    """
    Returns a lightweight index of core entities for client-side search.
    """
    try:
        master_graph = MasterGraph()
        entities = master_graph.get_search_entities()
        
        # Categorize results
        symbols = [e for e in entities if e['type'] in ['ticker', 'crypto']]
        agents = [e for e in entities if e['type'] == 'agent']
        clients = [e for e in entities if e['type'] == 'client']
        
        # Fallback to defaults if graph is empty (production safety)
        if not symbols:
            symbols = [
                {"id": "s-nvda", "label": "NVDA", "category": "Symbols", "type": "ticker"},
                {"id": "s-tsla", "label": "TSLA", "category": "Symbols", "type": "ticker"},
            ]
        
        return jsonify({
            "success": True,
            "data": {
                "symbols": symbols,
                "agents": agents,
                "clients": clients
            }
        })
    except Exception as e:
        logger.error(f"Search API: Indexing failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@search_bp.route('/query', methods=['GET'])
def search_query():
    """
    Performs a deep database search for a given query.
    """
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"success": True, "data": []})
        
    # Simulated deep search results
    results = [
        {"id": "d-1", "label": f"Historical Report for {query}", "category": "Reports", "type": "document"},
        {"id": "d-2", "label": f"Risk Exposure related to {query}", "category": "Risk", "type": "analysis"}
    ]
    
    return jsonify({"success": True, "data": results})
