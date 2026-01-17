"""
==============================================================================
FILE: web/api/politics_api.py
ROLE: Intelligence Dispatcher
PURPOSE:
    Expose Political Alpha data to the frontend.
    
    Endpoints:
    - GET /api/v1/politics/disclosures: Fetch latest congressional trades.
    - GET /api/v1/politics/alpha/<ticker>: Get alpha score for a specific ticker.
    
CONTEXT: 
    Phase 36: Political Alpha.
==============================================================================
"""

from flask import Blueprint, jsonify
from services.analysis.congress_tracker import get_congress_tracker

politics_bp = Blueprint('politics', __name__, url_prefix='/api/v1/politics')

@politics_bp.route('/disclosures', methods=['GET'])
def get_disclosures():
    tracker = get_congress_tracker()
    disclosures = tracker.fetch_latest_disclosures()
    return jsonify({
        "status": "success",
        "count": len(disclosures),
        "data": disclosures
    })

@politics_bp.route('/alpha/<ticker>', methods=['GET'])
def get_alpha_score(ticker):
    tracker = get_congress_tracker()
    score = tracker.get_political_alpha_signal(ticker)
    correlation = tracker.correlate_with_lobbying(ticker)
    
    return jsonify({
        "ticker": ticker,
        "alpha_score": score,
        "lobbying_intensity": correlation["lobbying_intensity"],
        "confidence": correlation["confidence"]
    })
