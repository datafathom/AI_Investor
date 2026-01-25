"""
==============================================================================
FILE: web/api/slack_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Slack messaging capabilities to the frontend.
==============================================================================
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging

from services.notifications.slack_service import get_slack_client

logger = logging.getLogger(__name__)

slack_api_bp = Blueprint('slack_api_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@slack_api_bp.route('/team/slack/message', methods=['POST'])
def post_message():
    """
    Post a message to a Slack channel.
    Body: { "channel": "#general", "text": "Hello World" }
    """
    data = request.get_json() or {}
    channel = data.get('channel')
    text = data.get('text')
    use_mock = request.args.get('mock', 'true').lower() == 'true'

    if not channel or not text:
        return jsonify({"error": "Missing 'channel' or 'text'"}), 400

    client = get_slack_client(mock=use_mock)
    
    try:
        result = _run_async(client.post_message(channel, text))
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to post Slack message: {e}")
        return jsonify({"error": str(e)}), 500

@slack_api_bp.route('/team/slack/channels', methods=['GET'])
def get_channels():
    """
    Get list of Slack channels.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    client = get_slack_client(mock=use_mock)
    
    try:
        result = _run_async(client.get_channels())
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to fetch Slack channels: {e}")
        return jsonify({"error": str(e)}), 500
