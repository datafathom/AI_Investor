"""
==============================================================================
FILE: web/api/discord_api.py
ROLE: Discord API REST Endpoints
PURPOSE: RESTful endpoints for Discord bot and webhook management.

INTEGRATION POINTS:
    - DiscordBot: Channel monitoring
    - DiscordWebhook: Alert dispatch

ENDPOINTS:
    GET /api/v1/discord/mentions/{ticker} - Get ticker mentions
    GET /api/v1/discord/hype/{ticker} - Get hype score
    POST /api/v1/discord/webhook/test - Test webhook
    POST /api/v1/discord/webhook/alert - Send alert

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

discord_bp = Blueprint('discord', __name__, url_prefix='/api/v1/discord')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@discord_bp.route('/mentions/<ticker>', methods=['GET'])
def get_mentions(ticker: str):
    """Get Discord mentions for a ticker."""
    try:
        limit = int(request.args.get('limit', 50))
        
        from services.social.discord_bot import get_discord_bot
        bot = get_discord_bot()
        
        mentions = _run_async(bot.get_recent_mentions(ticker, limit=limit))
        
        return jsonify({
            "ticker": ticker,
            "mentions": mentions,
            "count": len(mentions)
        })
    except Exception as e:
        logger.error(f"Failed to get mentions: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@discord_bp.route('/hype/<ticker>', methods=['GET'])
def get_hype(ticker: str):
    """Get hype score for a ticker."""
    try:
        from services.social.discord_bot import get_discord_bot
        bot = get_discord_bot()
        
        hype = _run_async(bot.get_hype_score(ticker))
        
        return jsonify(hype)
    except Exception as e:
        logger.error(f"Failed to get hype: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@discord_bp.route('/webhook/test', methods=['POST'])
def test_webhook():
    """Test webhook configuration."""
    try:
        data = request.json or {}
        webhook_url = data.get('webhook_url')
        
        if not webhook_url:
            return jsonify({"error": "Missing webhook_url"}), 400
        
        from services.communication.discord_webhook import get_discord_webhook
        webhook = get_discord_webhook(url=webhook_url)
        
        success = _run_async(webhook.send_alert(
            title="Test Alert",
            description="This is a test alert from AI Investor Terminal",
            color=0x00ff00
        ))
        
        return jsonify({
            "success": success,
            "message": "Test alert sent"
        })
    except Exception as e:
        logger.error(f"Webhook test failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@discord_bp.route('/webhook/alert', methods=['POST'])
def send_alert():
    """Send alert via webhook."""
    try:
        data = request.json or {}
        webhook_url = data.get('webhook_url')
        title = data.get('title')
        description = data.get('description')
        color = data.get('color', 0x00ff00)
        
        if not all([webhook_url, title, description]):
            return jsonify({"error": "Missing required fields"}), 400
        
        from services.communication.discord_webhook import get_discord_webhook
        webhook = get_discord_webhook(url=webhook_url)
        
        success = _run_async(webhook.send_alert(title, description, color))
        
        return jsonify({
            "success": success,
            "message": "Alert sent"
        })
    except Exception as e:
        logger.error(f"Failed to send alert: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
