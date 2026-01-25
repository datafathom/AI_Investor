"""
==============================================================================
FILE: web/api/debate_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Debate Chamber capabilities to the frontend.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from agents.debate_chamber_agent import get_debate_agent

logger = logging.getLogger(__name__)

debate_bp = Blueprint('debate_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@debate_bp.route('/debate/start', methods=['POST'])
def start_debate():
    """
    Start a new debate session.
    """
    data = request.json or {}
    ticker = data.get('ticker', 'SPY').upper()
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    agent = get_debate_agent(mock=use_mock)
    
    try:
        result = _run_async(agent.conduct_debate(ticker))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to run debate for %s: %s", ticker, e)
        return jsonify({"error": str(e)}), 500

@debate_bp.route('/debate/stream', methods=['GET'])
def stream_debate():
    """
    Get the current state of the debate.
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    agent = get_debate_agent(mock=use_mock)
    
    # Return current state from agent
    return jsonify({
        "status": "active",
        "transcript": agent.transcript,
        "consensus": agent.consensus
    })

@debate_bp.route('/debate/inject', methods=['POST'])
def inject_argument():
    """
    Inject a user argument into the debate.
    """
    data = request.json or {}
    argument = data.get('argument', '')
    
    # Mocking successful injection for now
    return jsonify({"status": "success", "message": "Argument received"})

@debate_bp.route('/debate/run/<ticker>', methods=['POST'])
def run_debate(ticker: str):
    """
    Trigger a new debate for a ticker.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    agent = get_debate_agent(mock=use_mock)
    
    try:
        result = _run_async(agent.conduct_debate(ticker))
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to run debate for %s: %s", ticker, e)
        return jsonify({"error": str(e)}), 500
