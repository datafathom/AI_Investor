from flask import Blueprint, jsonify, request
import logging

logger = logging.getLogger(__name__)
search_bp = Blueprint('search_api', __name__, url_prefix='/api/v1/search')

@search_bp.route('/index', methods=['GET'])
def get_search_index():
    """
    Returns a lightweight index of core entities for client-side search.
    """
    # In production, these would be fetched from DB/Cache
    # Symbols
    symbols = [
        {"id": "s-nvda", "label": "NVDA", "category": "Symbols", "type": "ticker"},
        {"id": "s-tsla", "label": "TSLA", "category": "Symbols", "type": "ticker"},
        {"id": "s-aapl", "label": "AAPL", "category": "Symbols", "type": "ticker"},
        {"id": "s-pltr", "label": "PLTR", "category": "Symbols", "type": "ticker"},
        {"id": "s-btc", "label": "BTC", "category": "Symbols", "type": "crypto"},
    ]
    
    # Agents
    agents = [
        {"id": "a-alpha", "label": "Alpha (Growth)", "category": "Agents", "type": "agent"},
        {"id": "a-guardian", "label": "Guardian (Hedge)", "category": "Agents", "type": "agent"},
        {"id": "a-observer", "label": "Observer (Macro)", "category": "Agents", "type": "agent"},
    ]
    
    # Common Clients (Simulated)
    clients = [
        {"id": "c-datafathom", "label": "DataFathom Corp", "category": "Clients", "type": "client"},
        {"id": "c-antigravity", "label": "Antigravity Research", "category": "Clients", "type": "client"},
    ]
    
    return jsonify({
        "success": True,
        "data": {
            "symbols": symbols,
            "agents": agents,
            "clients": clients
        }
    })

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
