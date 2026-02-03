"""
==============================================================================
FILE: web/api/incident_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes PagerDuty incident management to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.notifications.pagerduty_service import get_pagerduty_client

logger = logging.getLogger(__name__)

incident_api_bp = Blueprint('incident_api_bp', __name__, url_prefix='/api/v1/incident')

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@incident_api_bp.route('/ops/incidents/trigger', methods=['POST'])
def trigger_incident():
    """
    Trigger an incident manually.
    Body: { "title": "System Down", "urgency": "high" }
    """
    data = request.get_json() or {}
    title = data.get('title')
    urgency = data.get('urgency', 'high')
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not title:
        return jsonify({"error": "Missing 'title'"}), 400

    client = get_pagerduty_client(mock=use_mock)
    
    try:
        result = _run_async(client.trigger_incident(title, urgency))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to trigger incident: {e}")
        return jsonify({"error": str(e)}), 500

@incident_api_bp.route('/ops/incidents', methods=['GET'])
def get_incidents():
    """
    Get list of active incidents.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_pagerduty_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_incidents())
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to fetch incidents: {e}")
        return jsonify({"error": str(e)}), 500
