"""
==============================================================================
FILE: web/api/debate_api.py
ROLE: The Scribe
PURPOSE:
    Expose the Debate Chamber to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
from services.analysis.debate_chamber import get_debate_chamber

debate_bp = Blueprint('debate', __name__, url_prefix='/api/v1/analysis')

@debate_bp.route('/debate', methods=['POST'])
def trigger_debate():
    data = request.get_json() or {}
    ticker = data.get('ticker', 'SPY')
    summary = data.get('summary', 'Standard market overview.')
    
    chamber = get_debate_chamber()
    result = chamber.simulate_debate(ticker, summary)
    
    return jsonify(result)

@debate_bp.route('/debate/status', methods=['GET'])
def get_debate_status():
    # Currently stateless for simplicity
    return jsonify({"status": "ready"})
