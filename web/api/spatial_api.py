"""
==============================================================================
FILE: web/api/spatial_api.py
ROLE: The Spatial Navigator
PURPOSE:
    Expose endpoints for 3D/Spatial data visualization.
    Converts graph entities into 3D coordinate-ready JSON.
==============================================================================
"""

from flask import Blueprint, jsonify
import random
import logging

logger = logging.getLogger(__name__)
spatial_bp = Blueprint('spatial', __name__, url_prefix='/api/v1/spatial')

@spatial_bp.route('/portfolio', methods=['GET'])
def get_spatial_portfolio():
    """
    Returns portfolio holdings with synthetic 3D coordinates.
    In a real Neo4j setup, these coords would be derived from relationship clustering.
    """
    tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "GOOGL", "NVDA", "BTC", "ETH"]
    nodes = []
    links = []

    for i, ticker in enumerate(tickers):
        nodes.append({
            "id": ticker,
            "label": ticker,
            "val": random.randint(10, 50),
            "color": "#3b82f6" if i % 2 == 0 else "#10b981",
            "x": random.uniform(-50, 50),
            "y": random.uniform(-50, 50),
            "z": random.uniform(-50, 50)
        })

    # Create synthetic links
    for i in range(len(nodes) - 1):
        links.append({
            "source": nodes[i]["id"],
            "target": nodes[i+1]["id"]
        })

    return jsonify({
        "nodes": nodes,
        "links": links
    })

@spatial_bp.route('/status', methods=['GET'])
def get_xr_status():
    return jsonify({
        "status": "ready",
        "mode": "WebXRv1",
        "engine": "Three.js"
    })
