from flask import Blueprint, jsonify, request
import random
import logging

logger = logging.getLogger(__name__)
scanner_bp = Blueprint('scanner_api', __name__, url_prefix='/api/v1/scanner')

@scanner_bp.route('/matches', methods=['GET'])
def get_scanner_matches():
    """Returns the latest asset matches based on technical/AI signals."""
    # Simulation of real detector logic
    assets = ['NVDA', 'TSLA', 'AAPL', 'AMD', 'PLTR', 'COIN', 'MSFT', 'META', 'GOOGL', 'AMZN']
    sectors = ['TECH', 'CONSUMER', 'TECH', 'DATA', 'FINANCE', 'TECH', 'SOCIAL', 'TECH', 'RETAIL']
    signals = ['BULLISH', 'BEARISH', 'NEUTRAL']
    
    matches = []
    for i in range(10):
        symbol = random.choice(assets)
        matches.append({
            "id": i,
            "asset": symbol,
            "change": round(random.uniform(-5, 5), 2),
            "sector": random.choice(sectors),
            "signal": random.choice(signals),
            "timestamp": "2026-01-25T17:45:00Z"
        })
    
    return jsonify({"success": True, "data": matches})

@scanner_bp.route('/galaxy', methods=['GET'])
def get_galaxy_data():
    """Returns 3D correlation data for the Galaxy View."""
    # In production, this would use a correlation matrix from Polygon/AlphaVantage
    stars = []
    for i in range(100):
        stars.append({
            "id": i,
            "ticker": f"ASSET_{i}",
            "x": round(random.uniform(-400, 400), 2),
            "y": round(random.uniform(-250, 250), 2),
            "z": round(random.uniform(-500, 500), 2),
            "size": round(random.uniform(1, 5), 2),
            "color": "#10b981" if random.random() > 0.5 else "#ef4444"
        })
    return jsonify({"success": True, "data": stars})

@scanner_bp.route('/pulse', methods=['GET'])
def get_market_pulse():
    """Returns sector momentum data."""
    sectors = ['Tech', 'Finance', 'Energy', 'Health', 'Retail', 'Defense']
    data = []
    for s in sectors:
        data.append({
            "name": s,
            "change": round(random.uniform(-3, 3), 2)
        })
    return jsonify({"success": True, "data": data})
