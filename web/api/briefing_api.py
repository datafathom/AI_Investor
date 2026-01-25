"""
==============================================================================
FILE: web/api/briefing_api.py
ROLE: API Endpoint Layer (Flask)
PURPOSE: Exposes Morning Briefing capabilities to the frontend.
==============================================================================
"""

import asyncio
import logging
from flask import Blueprint, jsonify, request

from services.ai.briefing_generator import get_briefing_generator

logger = logging.getLogger(__name__)

briefing_bp = Blueprint('briefing_bp', __name__)

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

@briefing_bp.route('/briefing/daily', methods=['GET'])
def get_daily_briefing():
    """
    Get the daily morning briefing.
    Query: ?mock=true
    """
    use_mock = request.args.get('mock', 'true').lower() == 'true'
    generator = get_briefing_generator(mock=use_mock)
    
    try:
        result = _run_async(generator.get_daily_briefing())
        return jsonify(result)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Failed to fetch daily briefing: %s", e)
        return jsonify({"error": str(e)}), 500
